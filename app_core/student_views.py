from django.shortcuts import *
from .models import *
from django.contrib import messages


def student_register(request):
    is_student = False
    if request.method == "POST":
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        email = request.POST.get("email")
        address = request.POST.get("address")
        matric = request.POST.get("matric_no")
        student = Student_Account(user = request.user, first_name = first_name, last_name = last_name, email = email, address = address, matric = matric, is_student = True)
        student.save()
        return redirect("app:student-dashboard")
    if Student_Account.objects.filter(user = request.user).first():
        is_student = True
    context = {"is_student":is_student}
    return render(request, "student/student_register.html", context)



def student_dashboard(request):
    rooms = Rooms.objects.all()
    is_student = False
    student_user = Student_Account.objects.filter(user = request.user).first()
    if student_user:
        is_student = True
    context = {"is_student":is_student, "student_user": student_user, "rooms":rooms}
    return render(request, 'student/student_dashboard.html', context)


def payment(request):
    if request.method == "POST":
        card_number = request.POST.get("card_number")
        full_name = request.POST.get("fullname")
        bank = request.POST.get("bank")
        date_submit = request.POST.get("date_submit")
        amount = request.POST.get("amount")
        student = Student_Account.objects.get(user = request.user)
        deposit = Deposit(student = student, full_name = full_name, card_number = card_number, bank = bank, date_submit = date_submit, amount = amount)
        deposit.save()
        student.wallet += int(amount)
        student.save()
        messages.success(request, "Success!")
        return redirect(request.META.get("HTTP_REFERER"))

    context = {}
    return render(request, "student/payment.html", context)


def room_details(request, room_id):
    room = Rooms.objects.get(id = room_id)
    guidelines = Guideline.objects.all().first()
    print(guidelines)
    context = {"room":room, "guidelines":guidelines}
    return render(request, "student/room_details.html", context)


def accomodation_request(request):
    if request.method == "POST":
        room = request.POST.get("room_id")
        student = Student_Account.objects.get(user = request.user)
        room_obj = Rooms.objects.get(id = room)
        if student.wallet >= room_obj.charge:
            if Accomodation_Request.objects.filter(student = student).first():
                messages.error(request, "You already have a room allocated to you!")
                return redirect(request.META.get("HTTP_REFERER"))
            else:
                accomodation_obj = Accomodation_Request(student = student, room = room_obj)
                accomodation_obj.save()
                student.wallet -= room_obj.charge
                student.save()
                room_obj.is_available = False
                room_obj.save()

                messages.success(request, "Successfully Applied For This Room. Please continue to check your dashboard for your request confirmation!")
                return redirect(request.META.get("HTTP_REFERER"))
        
        else:
            messages.error(request, "Sorry! You do not have a enough balance to have this accomodation!")
            return redirect(request.META.get("HTTP_REFERER"))


def room_transfer(request):
    is_student = False
    is_roomed = False
    rooms = Rooms.objects.filter(is_available=True)
    student_user = Student_Account.objects.filter(user = request.user).first()
    if student_user:
        is_student = True
    if Accomodation_Request.objects.filter(student = student_user, approved=True).first():
        is_roomed = True
    if request.method == "POST":
        reason = request.POST.get("reason")
        room = request.POST.get("room_option")
        if RoomTransfer.objects.filter(student  = student_user).first():
            messages.error(request, "You already have a pending transfer request")
            return redirect(request.META.get("HTTP_REFERER"))
        
        room_obj = Rooms.objects.filter(id=room).first()
        if student_user.wallet >= room_obj.charge:
            student_user.wallet -= room_obj.charge
            student_user.save()
            room_transfer_obj = RoomTransfer(reason = reason, student = student_user, room = room_obj)
            room_transfer_obj.save()

            room_obj.is_available = False
            room_obj.save()
            messages.success(request, "Successfully requested for room transfer. Please continue to check your dashboard for your request confirmation!")
            return redirect(request.META.get("HTTP_REFERER"))
        else:
            messages.error(request, "Sorry, you can't apply for this room due to insufficient balance")
            return redirect(request.META.get("HTTP_REFERER"))

    context = {"is_student":is_student, "is_roomed":is_roomed, "student_user":student_user, "rooms":rooms}
    return render(request, "student/room_transfer.html", context)



def guest_stay(request):
    is_student = False
    is_roomed = False
    student_user = Student_Account.objects.filter(user = request.user).first()
    if student_user:
        is_student = True
    if Accomodation_Request.objects.filter(student = student_user, approved=True).first():
        is_roomed = True

    if request.method == "POST":
        full_name = request.POST.get("guest_name")
        address = request.POST.get("address")
        reason = request.POST.get("reason")
        date_from = request.POST.get("date_from")
        date_to = request.POST.get("date_to")
        
        if GuestStayRequest.objects.filter(student = student_user).first():
            messages.error(request, "You cannot apply for more than one guest stay")
            return redirect(request.META.get("HTTP_REFERER"))
        else:
            guest = GuestStayRequest(student = student_user, full_name=full_name, address=address, reason=reason, date_from=date_from, date_to=date_to)
            guest.save()
            messages.success(request, "Submitted Request Successfully, please check your dashboard for approval")
            return redirect(request.META.get("HTTP_REFERER"))


    context = {"is_student":is_student, "is_roomed":is_roomed}
    return render(request, "student/guest_stay.html", context)



def complaints(request):
    is_student = False
    student_user = Student_Account.objects.filter(user = request.user).first()
    if student_user:
        is_student = True
    if request.method == "POST":
        subject = request.POST.get("subject")
        message = request.POST.get("message")
        complain = Complaints(student = student_user, subject = subject, message = message)
        complain.save()
        messages.success(request, "Your ticket has being opened. Check your dashboard for response!")
    context = {"is_student":is_student, "student_user":student_user}
    return render(request, "student/complain.html", context)
            

def request_dashboard(request):
    student = Student_Account.objects.filter(user = request.user).first()
    room_transfers = RoomTransfer.objects.filter(student = student)
    guests = GuestStayRequest.objects.filter(student = student)
    complaints = Complaints.objects.filter(student = student)
    accomodations = Accomodation_Request.objects.filter(student = student)
    context = {"room_transfers":room_transfers, "guests":guests, "complaints":complaints, "accomodations":accomodations}
    return render(request, "student/request_dashboard.html", context)

def view_rents(request):
    rents = Rent.objects.all()
    return render(request, 'student/view_rents.html', {'rents': rents})

