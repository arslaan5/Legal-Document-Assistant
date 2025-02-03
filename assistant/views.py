from django.shortcuts import render, redirect
from .forms import UserRegistrationForm, UserLoginForm
from django.contrib.auth.hashers import make_password
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.tokens import default_token_generator
from django.urls import reverse
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.shortcuts import get_object_or_404
from .models import UserInfo
import os
from dotenv import load_dotenv
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from .scripts.utils import initialize_conversation, validate_query, generate_assistant_response, handle_ajax_request
import logging


load_dotenv()

logger = logging.getLogger(__name__)

@login_required
def query_view(request):
    """Handle user queries and generate responses."""
    initialize_conversation(request.session)

    if request.method == "POST":
        user_query = request.POST.get("query", "").strip()

        # Validate the query
        is_valid, error_message = validate_query(user_query)
        if not is_valid:
            response_html = error_message
        else:
            try:
                # Generate a response
                response_html = generate_assistant_response(request, user_query)
            except Exception as e:
                logger.error(f"Error generating response: {e}")
                response_html = "Sorry, an error occurred while generating a response."

        # Append the conversation to the session
        if user_query and response_html:
            request.session["conversation"].extend([
                {"role": "user", "content": user_query},
                {"role": "assistant", "content": response_html},
            ])
            request.session.modified = True

        # Handle AJAX requests
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return handle_ajax_request(user_query, response_html)

    return render(request, "index.html", {"conversation": request.session["conversation"]})


def home_view(request):
    return render(request, 'home.html')


def send_verification_email(request, user):
    """Send a verification email to the user."""
    token = default_token_generator.make_token(user)
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    verification_url = request.build_absolute_uri(
        reverse('verify_email', args=[uid, token])
    )

    # Render the HTML template with context
    html_content = render_to_string('verification_email.html', {
        'username': user.username,
        'verification_url': verification_url,
    })

    # Plain-text fallback
    text_content = f"""
    Hi {user.username},

    Please click the link below to verify your email address and activate your account:
    {verification_url}

    If you did not sign up for this account, you can ignore this email.
    """
    
    subject = 'Verify Your Email Address'

    # Send the email
    subject = 'Verify Your Email Address'
    from_email = os.getenv('EMAIL_HOST_USER')  # Ensure environment variable is set
    recipient_list = [user.email]

    email = EmailMultiAlternatives(
        subject=subject,
        body=text_content,
        from_email=from_email,
        to=recipient_list,
    )
    email.attach_alternative(html_content, "text/html")
    email.send()


def verify_email(request, uidb64, token):
    """Verify the user's email address."""
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = get_object_or_404(UserInfo, pk=uid)
    except (TypeError, ValueError, OverflowError, UserInfo.DoesNotExist):
        user = None

    if user and default_token_generator.check_token(user, token):
        user.is_active = True
        user.is_verified = True
        user.save()
        messages.success(request, 'Your email has been verified! You can now log in.')
        return redirect('login')
    else:
        messages.error(request, 'Invalid or expired verification link.')
        return redirect('home')


def register_view(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            # Hash the password before saving
            user = form.save(commit=False)
            user.password = make_password(form.cleaned_data['password'])
            user.is_active = False
            user.save()

            # Send verification email
            send_verification_email(request, user)

            messages.success(request, 'Registration successful! Please verify your email to activate your account.')
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
            user = form.get_user()
            if not user.is_active:  # Check if the user has verified their email
                messages.error(request, 'Your email is not verified. Please check your inbox and verify your email before logging in.')
                return redirect('login')
            
            # User is authenticated and email is verified
            login(request, user)
            return redirect('index')
        else:
            # Form is invalid or authentication failed
            messages.error(request, 'Invalid username or password.')
    else:
        form = UserLoginForm()

    return render(request, 'login.html', {'form': form})

