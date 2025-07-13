from django.shortcuts import render
from .models import Contact
from .serializers import ContactSerializers, InputSerializer, OutputSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q  # for filtering 
from collections import OrderedDict
from drf_yasg.utils import swagger_auto_schema

# Create your views here.

class ContactView(APIView):
    permission_classes=[AllowAny]
    @swagger_auto_schema(query_serializer=ContactSerializers)
    def get(self,request):
        contacts = Contact.objects.all()
        serializer = ContactSerializers(contacts, many=True)
        if contacts:
            return Response({
                'contacts': serializer.data
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                "contacts":Contact.objects.none()
            }, status=status.HTTP_204_NO_CONTENT)


        


            

class SolutionView3(APIView):
    
    permission_classes=[AllowAny]
    @swagger_auto_schema(
        request_body=InputSerializer,
        responses={200: OutputSerializer}
    )
    def post(self, request):
        email =request.data.get('email')
        phone = request.data.get('phoneNumber')
        email = (email or "").strip().lower()
        phone = (phone or "").strip()
        emails=[]
        phonenumbers=[]
        secondaryContactIds=[]
        print(f"{email}\n{phone}\n")

        if email!="" and phone!="" and  Contact.objects.filter(Q(phone=phone) | Q(email=email)).exists():
            #either email or phone matches
            if Contact.objects.filter(Q(phone=phone) | Q(email=email)).exists(): 
                renderContacts = Contact.objects.filter(Q(phone=phone) | Q(email=email)).order_by('createdAt')#all the instances containing emale or phone
                print(f"rendered all contacts from db matching email or phone \n")


                for contact in renderContacts:
                    if contact.phone==phone and contact.email==email:
                        print(f"email and phone both matches!\n")
                        emails.insert(0,contact.email) if contact.linkPrecedence=='primary' else emails.append(contact.email)
                        phonenumbers.insert(0, contact.phone) if contact.phone=='primary' else phonenumbers.append(contact.phone)
                        if contact.linkedId:
                            secondaryContactIds.append(contact.linkedId.id)
                    #existing phone matching in db
                    elif contact.email==email and contact.phone!=phone and Contact.objects.filter(phone=phone).exists():#if email matches one with one contact then look for phone to match 
                        print(f"Email matches but phone not and a contact is existing weith same phone number in request. \n")
                        for i , c in enumerate(renderContacts):
                            if c.phone==phone and contact.id!=c.id:
                                print(f"phone matches with request data  , a contact is matched with another contact. and should be linked\n")
                                if contact.createdAt < c.createdAt:
                                    c.linkPrecedence='secondary'
                                    c.linkedId=contact if contact.linkPrecedence=='primary' else contact.linkedId
                                    c.save()
                                    print(f"Saved \n")
                                elif contact.createdAt > c.createdAt:
                                    contact.linkPrecedence='secondary'
                                    contact.linkedId=c if c.linkPrecedence=='precedence' else c.linkedId
                                    contact.save()
                                    print(f"Saved \n")
                    elif contact.phone==phone and contact.email!=email and Contact.objects.filter(email=email).exists():
                        print(f" contact's phone is matching with request phone but not email and have a another contact with same email but different number. \n")
                        for i, c in enumerate(renderContacts):
                            if c.email==email and contact.id!= c.id:
                                print(f"Found the contact have same email but different phone ")
                                if contact.createdAt > c.createdAt:
                                    contact.linkPrecedence='secondary'
                                    contact.linkedId=c if c.linkPrecedence=='primary' else c.linkedId
                                    contact.save()
                                    print(f"Saved \n")
                                elif contact.createdAt < c.createdAt:
                                    c.linkedId=contact if contact.linkPrecedence=='primary' else contact.linkedId
                                    c.linkPrecedence='secondary'
                                    c.save()
                                    print(f"Saved \n")
                    #not existing any phone matching to it in db but have email matching to db
                    elif contact.email==email and contact.phone!=phone and not Contact.objects.filter(phone=phone).exists():
                        print(f"email is matched with one contact but phone is not matching and do not have matching phone new instance created. \n")
                        new_contact= Contact.objects.create(email=email, phone=phone, linkedId=contact, linkPrecedence='secondary')#new secondarycontact
                        new_contact.save()
                        print(f" New Saved \n")
                    #not existing any email to db but have phone matching to db
                    elif contact.phone==phone and contact.email!=email and not Contact.objects.filter(email=email).exists():
                        print(f"phone is matched with one contact but email is not matching and do not have matching email new instance created. \n")
                        new_contact= Contact.objects.create(email=email, phone=phone, linkedId=contact, linkPrecedence='secondary')#new secondary contact
                        new_contact.save()
                        print(f"New Saved \n")
        # no instance found in db
        else:
            if email and not phone and email!="" and not Contact.objects.filter(email=email).exists():
                newContact=Contact.objects.create(email=email)
                newContact.save()
                print(f"New Saved \n")
            if not email and phone and phone!="" and not Contact.objects.filter(phone=phone).exists():
                newContact= Contact.objects.create(phone=phone)
                newContact.save()
                print(f"New Saved \n")
            if email and phone:
                newContact=Contact.objects.create(phone=phone, email=email)
                newContact.save()
                print(f"New Saved \n")

        allcontacts= Contact.objects.filter(Q(linkedId__phone=phone) | Q(linkedId__email=email) | Q(email=email) | Q(phone=phone)).distinct()
        
        primaryContactNumber=allcontacts[0].linkedId.phone if allcontacts[0].linkedId else phone
        primaryEmail=allcontacts[0].linkedId.email if allcontacts[0].linkedId else email
        extractedAllContacts= Contact.objects.filter(Q(linkedId__phone=primaryContactNumber) | Q(linkedId__email__exact=primaryEmail) | Q(email=primaryEmail) | Q(phone=primaryContactNumber)).distinct()
            # primaryContactId, emails, phoneNumbers, secondaryContactIds= self.formatted_response(extractedAllContacts)
            # return Response({
            #     'contact': {
            #     "primaryContactId":primaryContactId,
            #     "emails":(emails),
            #     "phoneNumbers": (phoneNumbers),
            #     "secondaryContactIds":set(secondaryContactIds)
            # })
        
        # extractedAllContacts= Contact.objects.filter(Q(linkedId__phone=phone) | Q(linkedId__email__exact=email) | Q(email=email) | Q(phone=phone)).distinct()
        primaryContactId, emails, phoneNumbers, secondaryContactIds= self.formatted_response(extractedAllContacts)
        return Response({
                'contact': {
                "primaryContactId":primaryContactId,
                "emails":(emails),
                "phoneNumbers": (phoneNumbers),
                "secondaryContactIds":set(secondaryContactIds)
            }
            }, status=status.HTTP_200_OK)




    def formatted_response(self,contacts):
        emails=[]
        phoneNumbers=[]
        secondaryContactIds=[]
        primaryContactId=None
        
       
        for contact in contacts:
            if contact.linkPrecedence=='primary':
                primaryContactId=contact.id
                emails.insert(0,contact.email)
                phoneNumbers.insert(0, contact.phone)
            elif contact.linkPrecedence=='secondary':
                secondaryContactIds.append(contact.id)
                
                emails.append(contact.email)
                phoneNumbers.append(contact.phone)
                
                
        emails       = list(OrderedDict.fromkeys(emails))
        phoneNumbers = list(OrderedDict.fromkeys(phoneNumbers))
        secondaryContactIds= list(OrderedDict.fromkeys(secondaryContactIds))
        return primaryContactId,(emails),(phoneNumbers),(secondaryContactIds)