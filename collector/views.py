from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Person
from .forms import PersonForm
import openpyxl
from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponse

from django.contrib.auth import get_user_model
def create_superuser(request):
    User = get_user_model()

    if User.objects.filter(username="admin").exists():
        return HttpResponse("Superuser already exists")

    User.objects.create_superuser(
        username="admin",
        email="admin@example.com",
        password="Admin@123"
    )

    return HttpResponse("Superuser created")
# 1. Home Page: Shows list of all registered people
@login_required
def home(request):
    # Try to get the current user's profile to see if they exist/are locked
    try:
        current_user_profile = Person.objects.get(user=request.user)
    except Person.DoesNotExist:
        current_user_profile = None

    # Get all locked (finalized) profiles to show in the list
    people = Person.objects.filter(is_locked=True)
    
    return render(request, 'collector/home.html', {
        'people': people,
        'my_profile': current_user_profile
    })

# 2. Data Entry Page
@login_required
def fill_form(request):
    # Get existing profile or None
    try:
        person = request.user.person
        if person.is_locked:
            return redirect('home') # Block access if already locked
    except Person.DoesNotExist:
        person = None

    if request.method == 'POST':
        form = PersonForm(request.POST, instance=person)
        if form.is_valid():
            # Save, but don't commit to DB yet so we can attach the user
            profile = form.save(commit=False)
            profile.user = request.user
            profile.save()
            return redirect('review_person') # Go to re-check page
    else:
        form = PersonForm(instance=person)

    return render(request, 'collector/form.html', {'form': form})

# 3. Re-check / Confirmation Page
@login_required
def review_person(request):
    person = get_object_or_404(Person, user=request.user)
    
    if person.is_locked:
        return redirect('home')

    if request.method == 'POST':
        # User clicked "Confirm"
        person.is_locked = True
        person.save()
        return redirect('home')


    return render(request, 'collector/review.html', {'person': person})


# 4. Superuser Export View
@user_passes_test(lambda u: u.is_superuser)
def export_excel(request):
    # 1. Create a workbook and sheet
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Registered Users"

    # 2. Add Headers (Make them bold if you want, but simple is fine)
    headers = ['Name', 'Address', 'Email', 'Phone', 'Technology']
    ws.append(headers)

    # 3. Query the data (Only locked/confirmed users)
    people = Person.objects.filter(is_locked=True)

    # 4. Write data rows
    for person in people:
        ws.append([
            person.name,
            person.address,
            person.email,
            person.phone_number,
            person.get_preferred_technology_display() # Gets the label "Python" instead of "python"
        ])

    # 5. Prepare the response
    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    # This sets the filename
    response['Content-Disposition'] = 'attachment; filename=registry_data.xlsx'
    
    # Save the workbook to the response
    wb.save(response)
    
    return response
