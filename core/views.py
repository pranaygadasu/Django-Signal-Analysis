from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from .models import TestModel
import time
import threading
from django.db import transaction


# 1. Test sync behavior
def test_signal(request):
    start = time.time()

    TestModel.objects.create(name="test")

    end = time.time()
    return HttpResponse(f"Time taken: {end - start}")


# 2. Test thread behavior
def test_thread(request):
    print("View Thread:", threading.get_ident())

    TestModel.objects.create(name="thread test")

    return HttpResponse("Check terminal for thread IDs")


# 3. Test transaction behavior
def test_transaction(request):
    try:
        with transaction.atomic():
            TestModel.objects.create(name="txn test")
            raise Exception("Force rollback")
    except:
        pass

    exists = TestModel.objects.filter(name="txn test").exists()

    return HttpResponse(f"Exists after rollback: {exists}")
