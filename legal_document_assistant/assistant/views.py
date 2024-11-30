from django.shortcuts import render, redirect
from django.http import JsonResponse
from .scripts.data_retriever import retrieve_relevant_chunks
from .scripts.response_handler import generate_response
from markdown import markdown
from .forms import UserRegistrationForm, UserLoginForm
from django.contrib.auth.hashers import make_password
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required


@login_required
def query_view(request):
    if "conversation" not in request.session:
        # Initialize conversation history in the session
        request.session["conversation"] = []

    if request.method == "POST":
        user_query = request.POST.get("query")
        
        if len(user_query) < 5:
            response_html = "Query too short. Please ask a question or provide more context."

        # Retrieve relevant chunks from Pinecone
        relevant_chunks = retrieve_relevant_chunks(user_query)
        
        if relevant_chunks:
            # Generate a response using LangChain
            response = generate_response(user_query, relevant_chunks)
            if hasattr(response, "content"):  # Check if it's an AIMessage or similar
                response = response.content
        else:
            response = "Sorry, I could only answer your legal queries."
        
        # Convert response to HTML from Markdown
        response_html = markdown(response)

        if user_query and response_html:
            # Append the user's query and assistant's response to the session
            request.session["conversation"].append({"role": "user", "content": user_query})
            request.session["conversation"].append({"role": "assistant", "content": response_html}) 
        else:
            response_html = "Sorry, I didn't understand your query. Please rephrase it."

        # Save the session
        request.session.modified = True

        # If the request is AJAX, return only the new messages
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                "user_message": {"role": "user", "content": user_query},
                "assistant_message": {"role": "assistant", "content": response_html},
            })

    return render(request, "index.html", {"conversation": request.session["conversation"]})

@login_required
def end_session(request):
    # Manually clear the session data
    request.session.flush()

    # Redirect to the home page or any other page
    return redirect('index')  # You can change 'home' to any URL name


def home_view(request):
    return render(request, 'home.html')


def register_view(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            # Hash the password before saving
            user = form.save(commit=False)
            user.password = make_password(form.cleaned_data['password'])
            user.save()
            messages.success(request, 'Registration successful! You can now log in.')
            return redirect('login')
        else:
            # If the form is not valid, show error messages
            messages.error(request, 'Error in registraion.')
    else:
        form = UserRegistrationForm()

    return render(request, 'register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            # User is authenticated and validated
            user = form.get_user()
            login(request, user)
            return redirect('index')
        else:
            # Form is invalid or authentication failed
            messages.error(request, 'Invalid username or password')
    else:
        form = UserLoginForm()

    return render(request, 'login.html', {'form': form})
