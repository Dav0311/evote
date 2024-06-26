from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .models import Candidate, Vote, Student
from django.db.models import Count
from django.urls import reverse
from .models import FingerprintData 
from django.contrib.auth.models import User 
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.backends import ModelBackend
from .forms import StudentLoginForm 



def student_login_view(request):
    if request.method == "POST":
        form = StudentLoginForm(request.POST)
        if form.is_valid():
            firstname = form.cleaned_data.get('firstname')
            registrationNo = form.cleaned_data.get('registrationNo')
            user = authenticate(request, firstname=firstname, registrationNo=registrationNo)
            if user is not None:
                login(request, user)
                # Redirect to some page after successful login
                return render(request, "polls/index.html")
                
            else:
                # Handle invalid login credentials
                return render(request, "polls/student.html", {
                    "form": form,
                    "message": "Invalid login credentials. Please try again."
                })
    else:
        form = StudentLoginForm()
    return render(request, "polls/student.html", {"form": form})

# Create your views here.
def index(request):
    candidates = Candidate.objects.annotate(vote_count=Count('id'))
    students = Student.objects.annotate(total=Count('id'))

    context ={
        "candidates": candidates,
        "students": students
    }
    return render(request, "polls/index.html", context)


def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return render(request, "polls/addcandidate.html")
        else:
            return render(request, "polls/login.html", {
                "message": "Invalid user credentials. Please register as a user."
            })
    return render(request, "polls/login.html")




def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            if user is not None:
                login(request, user)
                # Redirect to a success page
                return redirect('addcandidate')
    else:
        form = UserCreationForm()
    return render(request, 'polls/signup.html', {'form': form})


def logout_view(request):
    logout(request)
    return render (request, "polls/index.html",{
        "message":"user has been logged out"
    })

# def register_fingerprint(request):
#     if request.method == 'POST':
       
#         fingerprint_data = fingerprint_sensor_library.capture_fingerprint()

       
#         fingerprint_instance = FingerprintData(data=fingerprint_data)
#         fingerprint_instance.save()

#         # Redirect to a success page or another view
#         return redirect('success_page')

#     return render(request, 'polls/addvoters.html')


#@login_required 
def addcandidate_view(request):
    if request.method == 'POST' and request.FILES.get('image'):
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        registrationNo = request.POST.get('registrationNo') 
       
        image = request.FILES['image']
        
       
        candidate = Candidate(
            
            image=image,
            firstname=firstname,
            lastname=lastname,
            registrationNo=registrationNo
        )
        candidate.save()
        
        return render(request, "polls/addcandidate.html", {
            'message': 'Candidate added successfully.'
        })
    return render(request, "polls/addcandidate.html")



#@login_required 
def addelection_view(request):
    candidates = Candidate.objects.all()  # Use 'candidates' instead of 'candidate'
    return render(request, "polls/addelection.html", {
        'candidates': candidates  # Use 'candidates' here
    })

# def vote(request, candidate_id):
#     candidate = get_object_or_404(Candidate, pk=candidate_id)
    
#     try: 
#         selected_candidate = candidate.choice_set.get(pk=request.POST['choice'])
#     except (KeyError, Choice.DoesNotExist):
#         return render(request, 'polls/result.html', {
#             'candidate': candidate,
#             'error_message': 'You did not make a valid vote.'
#         })
#     else:
#         selected_candidate.votes += 1
#         selected_candidate.save()
#         return render(request, 'polls/addelection.html', {
#             'votemessage': 'Your vote has been saved.'
#         })

#@login_required 

def vote(request):
    if request.method == 'POST':
        candidate_id = request.POST.get('choice')  # Get the selected candidate's ID
        candidate = get_object_or_404(Candidate, pk=candidate_id)
        
        # Create a new Vote instance and associate it with the logged-in student
        Vote.objects.create(candidate=candidate, voter=request.user)
        
        # Increment the candidate's vote count
        candidate.vote_count += 1
        candidate.save()
        
        # Redirect to a different URL after successful vote
        return redirect('polls:addelection')  # Replace 'polls:addelection' with your appropriate URL name

    # Handle cases where the form is not submitted via POST
    return HttpResponseRedirect(reverse('polls:poll.html'), {
        "message": 'Failed to confirm your vote'
    })  

#@login_required 
def addvoter_view(request):
    if request.method == 'POST' and request.FILES.get('image'):
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        registrationNo = request.POST.get('registrationNo') 
       
        image = request.FILES['image']
        
       
        student = Student(
            
            image=image,
            firstname=firstname,
            lastname=lastname,
            registrationNo=registrationNo
        )
        student.save()
        
        return render(request, "polls/addvoters.html", {
            'message': 'Candidate added successfully.'
        })
    return render(request, "polls/addvoters.html")



# def result_view(request):
#     # Assuming you have a Candidate model with a ForeignKey to votes
#     candidates = Candidate.objects.annotate(vote_count=Count('vote'))

#     # Render the template with the candidates queryset
#     return render(request, 'polls/result.html', {'candidates': candidates})




def result_view(request):
    candidates = Candidate.objects.all()
    
    # Count votes for each candidate
    vote_counts = {}
    for candidate in candidates:
        vote_count = Vote.objects.filter(candidate=candidate).count()
        vote_counts[candidate] = vote_count
    
    return render(request, 'polls/result.html', {'candidates': candidates, 'vote_counts': vote_counts})

#@login_required  # Ensure the user is logged in (authenticated) to cast a vote
# def cast_vote(request, candidate_id):
#     # Get the selected candidate
#     candidate = get_object_or_404(Candidate, pk=candidate_id)
    
#     # Create a new Vote instance and associate it with the logged-in student
#     Vote.objects.create(candidate=candidate, voter=request.user)
    
#     # Redirect to a success page or display a success message
#     return redirect('success_page')

def count_votes():
    """
    Function to count votes for each candidate.
    Returns a dictionary where keys are candidate IDs and values are vote counts.
    """
    vote_counts = {}
    for candidate in Candidate.objects.all():
        vote_count = Vote.objects.filter(candidate=candidate).count()
        vote_counts[candidate.id] = vote_count
    return vote_counts  
class StudentBackend(ModelBackend):
    def authenticate(self, request, firstname=None, registrationNo=None):
        try:
            student = Student.objects.get(firstname=firstname, registrationNo=registrationNo)
            return student
        except Student.DoesNotExist:
            return None

