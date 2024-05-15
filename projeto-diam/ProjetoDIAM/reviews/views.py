from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from .models import Review, Gender
from django.contrib.auth import authenticate, login, logout, models
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from django.urls import reverse
from .models import Reviewer, Comment, Rating
from django.db.models import Avg
from django.core.files.storage import FileSystemStorage
from django.utils import timezone
from django.contrib.auth.hashers import check_password


def homepage(request):
    latest_review_list = Review.objects.order_by('-pub_data')
    context = {'latest_review_list': latest_review_list}
    gender_list = Gender.objects.order_by('gender_category')
    context1 = {'gender_list': gender_list}
    context.update(context1)
    for review in latest_review_list:
        review.avg_rating = review.rating_set.all().aggregate(Avg('rating_number'))['rating_number__avg']
    if request.user.is_authenticated:
        current_reviewer = Reviewer.objects.get(user=request.user)
        following_reviewers = current_reviewer.following.all()
        following_comments = Comment.objects.filter(reviewer__in=following_reviewers).order_by('-pub_data')
        context2 = {'following_comments': following_comments}
        context.update(context2)
        return render(request, 'reviews/homepage.html', context)
    else:
        return render(request, 'reviews/homepage.html', context)


def search(request):
    reviews = Review.objects.all()
    reviewers = Reviewer.objects.all()
    gender_list = Gender.objects.order_by('gender_category')
    context = {'gender_list': gender_list}
    search_reviews = []
    search_reviewers = []
    search_gender = []
    if request.method == 'POST':
        search = request.POST['search']
        context1 = {'search': search}
        context.update(context1)
        for review in reviews:
            if search.lower() in review.review_title.lower():
                search_reviews.append(review)
        context2 = {'search_reviews': search_reviews}
        context.update(context2)
        for reviewer in reviewers:
            if search.lower() in reviewer.user.username.lower():
                search_reviewers.append(reviewer)
        context3 = {'search_reviewers': search_reviewers}
        context.update(context3)
        for gender in gender_list:
            if search.lower() == gender.gender_category.lower():
                for review in gender.reviews.all():
                    search_gender.append(review)
        context4 = {'search_gender': search_gender}
        context.update(context4)
        return render(request, 'reviews/search.html', context)
    return render(request, 'reviews/search.html', context)


def search_gender(request, gender_id):
    gender_list = Gender.objects.order_by('gender_category')
    context = {'gender_list': gender_list}
    gender = Gender.objects.get(id=gender_id)
    search = gender.gender_category
    context2 = {'search': search}
    context.update(context2)
    search_gender = []
    for review in gender.reviews.all():
        search_gender.append(review)
    context3 = {'search_gender': search_gender}
    context.update(context3)
    return render(request, 'reviews/search.html', context)


def login_register(request):
    return render(request, 'reviews/login.html')


def review(request, review_id):
    review = get_object_or_404(Review, pk=review_id)
    context = {'review': review}
    comments = Comment.objects.filter(review=review)
    context1 = {'comments': comments}
    context.update(context1)
    gender_list = Gender.objects.order_by('gender_category')
    context2 = {'gender_list': gender_list}
    context.update(context2)
    review.avg_rating = review.rating_set.all().aggregate(Avg('rating_number'))['rating_number__avg']
    if request.method == 'POST':
        for comment in comments:
            if comment.reviewer.id == request.user.reviewer.id:
                context3 = {'error_message': "This User already commented this movie!"}
                context.update(context3)
                return render(request, 'reviews/review.html', context)

        try:
            comment_text = request.POST['comment_text']
            rating_number = request.POST['rating']
            if rating_number == "":
                context3 = {'error_message': "Rate the movie first!"}
                context.update(context3)
                return render(request, 'reviews/review.html', context)
            user = request.user
            reviewer = Reviewer.objects.get(user=user)
            rating = Rating(rating_number=rating_number, review=review, reviewer=reviewer)
            rating.save()
            comment = review.comment_set.create(comment_text=comment_text, review=review, pub_data=timezone.now(),
                                                reviewer=reviewer)
            comment.save()
        except KeyError:
            # Redisplay the form with an error message
            return render(request, 'reviews/review.html', {'error_message': "Não escreveu nenhum comentário"})
        else:
            return HttpResponseRedirect(reverse('reviews:review', args=(review.id,)))
    else:
        return render(request, 'reviews/review.html', context)


def createreview(request):
    gender_list = Gender.objects.order_by('gender_category')
    context = {'gender_list': gender_list}
    if request.method == 'POST':
        review_title = request.POST['review_title']
        pub_data = request.POST['pub_data']
        overview = request.POST['overview']
        review = Review(review_title=review_title, pub_data=pub_data, overview=overview)
        review.save()
        genres = request.POST.getlist('opcoes')
        for genre in genres:
            genre = Gender.objects.get(gender_category=genre)
            genre.reviews.add(review)
        if 'myfile' in request.FILES:
            print("olá")
            myfile = request.FILES['myfile']
            fs = FileSystemStorage()
            filename = fs.save(myfile.name, myfile)
            uploaded_file_url = fs.url(filename)
            review.photo = uploaded_file_url.replace('/reviews', '', 1)
            review.save()
        return HttpResponseRedirect(reverse('reviews:homepage'))
    else:
        return render(request, 'reviews/createreview.html', context)


def loginview(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            # direccionar para página de sucesso
            return HttpResponseRedirect(reverse('reviews:homepage'))
        else:
            # direccionar para página de insucesso
            return render(request, 'reviews/login.html',
                          {'error_message': "Incorrect Username or Password, please insert the right inputs!"})
    else:
        return render(request, 'reviews/login.html')

def registerview(request):
    try:
        new_username = request.POST['new_username']
        new_password = request.POST['new_password']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        if (new_username == "" or first_name == "" or last_name == "" or email == "" or new_password == ""):
            return render(request, 'reviews/login.html', {'error_message': "Por favor preencha todos os campos."})
        elif (len(new_username) > 15):
            return render(request, 'reviews/login.html', {'error_message': "O username não pode conter mais de 15 caracteres"})
        elif ( " " in new_username):
            return render(request, 'reviews/login.html', {'error_message': "O nome de utilizador não pode conter espaços em branco."})
        elif ( not "@" in email or not "." in email):
            return render(request, 'reviews/login.html', {'error_message': "Introduza um email válido"})
        elif (len(new_password) < 8):
            return render(request, 'reviews/login.html', {'error_message': "A senha deve ter pelo menos 8 caracteres."})
        u = User.objects.create_user(username=new_username, email=email, password=new_password, first_name=first_name,
                                     last_name=last_name)
        u.save()
        ut = Reviewer(user=u)
        ut.save()
    except KeyError:
        # Redisplay the form with an error message
        return render(request, 'reviews/login.html', {'error_message': "Não escreveu nenhuma opção"})
    else:
        if u is not None:
            login(request, u)
        return HttpResponseRedirect(reverse('reviews:homepage'))

def logoutview(request):
    logout(request)
    return HttpResponseRedirect(reverse('reviews:homepage'))


def profile(request, profile_id):
    reviewer = get_object_or_404(Reviewer, pk=profile_id)
    context = {'reviewer': reviewer}
    user_comments = Comment.objects.filter(reviewer=reviewer)
    context1 = {'user_comments': user_comments}
    context.update(context1)
    if request.user.is_authenticated:
        user = request.user.reviewer
        exists = user.following.filter(id=reviewer.id).exists()
        context2 = {'exists': exists}
        context.update(context2)
    return render(request, 'reviews/profile.html', context)


def editar_perfil(request):
    if request.method == 'POST':
        user = request.user
        new_first_name = request.POST['first_name']
        user.first_name = new_first_name
        new_last_name = request.POST['last_name']
        user.last_name = new_last_name
        new_email = request.POST['email']
        user.email = new_email
        current_password = request.POST['current_password']
        new_password = request.POST['new_password']
        user.save()
        if (check_password(current_password, user.password) and new_password != ""):
            user.set_password(new_password)
            user.save()
            user = authenticate(username=request.user.username, password=new_password)
            login(request, user)
        elif (not check_password(current_password, user.password) and current_password != ""):
            return render(request, 'reviews/editar_perfil.html', {'error_message': "Current Password Incorrect"})
        elif (check_password(current_password, user.password) and new_password == ""):
            return render(request, 'reviews/editar_perfil.html', {'error_message': "Invalid New Password"})
        elif 'myfile' in request.FILES:
            myfile = request.FILES['myfile']
            fs = FileSystemStorage()
            filename = fs.save(myfile.name, myfile)
            uploaded_file_url = fs.url(filename)
            reviewer = request.user.reviewer
            reviewer.photo = uploaded_file_url.replace('/reviews', '', 1)
            reviewer.save()
        return render(request, 'reviews/editar_perfil.html')
    return render(request, 'reviews/editar_perfil.html')


def deletereview(request, review_id):
    review = get_object_or_404(Review, pk=review_id)
    try:
        review.delete()
    except KeyError:
        # Redisplay the form with an error message
        return render(request, 'reviews/homepage.html', {'error_message': "Erro"})
    else:

        return HttpResponseRedirect(reverse('reviews:homepage'))


def deletecomment(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    reviewer = comment.reviewer
    review = comment.review
    rating = Rating.objects.filter(review=review, reviewer=reviewer)
    try:
        comment.delete()
        rating.delete()
    except KeyError:
        # Redisplay the form with an error message
        return render(request, 'reviews/review.html', {'error_message': "Erro"})
    else:

        return HttpResponseRedirect(reverse('reviews:review', args=(comment.review.id,)))


def follow(request, reviewer_id):
    followed = get_object_or_404(Reviewer, pk=reviewer_id)
    user = request.user
    reviewer = Reviewer.objects.get(user=user)
    reviewer.following.add(followed)
    reviewer.save()
    return HttpResponseRedirect(reverse('reviews:profile', args=(reviewer_id,)))


def unfollow(request, reviewer_id):
    followed = get_object_or_404(Reviewer, pk=reviewer_id)
    user = request.user
    reviewer = Reviewer.objects.get(user=user)
    reviewer.following.remove(followed)
    reviewer.save()
    return HttpResponseRedirect(reverse('reviews:profile', args=(reviewer_id,)))


def termsofservice(request):
    return render(request, 'reviews/termsofservice.html')

def aboutus(request):
    return render(request, 'reviews/aboutus.html')

def contact(request):
    return render(request, 'reviews/contact.html')
