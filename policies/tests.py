import datetime

from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from .models import Policy
from .serializers import PolicySerializer


def create_policy(customer_name, policy_type, days_offset=0):
    """
    Creates a policy with the given customer name, policy type and expiry date of now + days_offset.
    """
    expiry_date = timezone.now().date() + datetime.timedelta(days=days_offset)
    return Policy.objects.create(customer_name=customer_name, policy_type=policy_type, expiry_date=expiry_date)


class PolicyModelTests(TestCase):
    def test_is_expired_with_valid_policy(self):
        """
        is_expired() should return False for policies whose expiry_date is in the future.
        """
        date = timezone.now().date() + datetime.timedelta(days=1)
        policy = Policy(expiry_date=date)
        self.assertIs(policy.is_expired(), False)

    def test_is_expired_with_about_to_expire_policy(self):
        """
        is_expired() should return False for policies whose expiry_date is today.
        """
        date = timezone.now().date()
        policy = Policy(expiry_date=date)
        self.assertIs(policy.is_expired(), False)

    def test_is_expired_with_expired_policy(self):
        """
        is_expired() should return True for policies whose expiry_date is before today.
        """
        date = timezone.now().date() - datetime.timedelta(days=1)
        policy = Policy(expiry_date=date)
        self.assertIs(policy.is_expired(), True)


class PolicyViewSetTests(TestCase):
    def test_list_with_no_policies(self):
        """
        If no policies exist, an appropriate message is displayed.
        """
        url = reverse("policies-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, b'[]')

    def test_list_with_valid_policy(self):
        """
        If a single valid policy exists, it should be listed.
        """
        policy = create_policy(customer_name="Customer", policy_type=Policy.Type.AUTO)
        expected_content = PolicySerializer(instance=[policy], many=True).data
        url = reverse("policies-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, expected_content)

    def test_create_with_blank_customer_name(self):
        url = reverse("policies-list")
        data = {
            "customer_name": "",
            "policy_type": Policy.Type.AUTO,
            "expiry_date": timezone.now().date().isoformat()
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 400)
        self.assertIn('customer_name', response.data)
        self.assertQuerySetEqual(Policy.objects.all(), [])

    def test_create_with_null_customer_name(self):
        url = reverse("policies-list")
        data = {
            "policy_type": Policy.Type.AUTO,
            "expiry_date": timezone.now().date().isoformat()
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 400)
        self.assertIn('customer_name', response.data)
        self.assertQuerySetEqual(Policy.objects.all(), [])

    def test_create_with_null_policy_type(self):
        url = reverse("policies-list")
        data = {
            "customer_name": "Customer",
            "expiry_date": timezone.now().date().isoformat()
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 400)
        self.assertIn('policy_type', response.data)
        self.assertQuerySetEqual(Policy.objects.all(), [])

    def test_create_with_invalid_policy_type(self):
        url = reverse("policies-list")
        data = {
            "customer_name": "Customer",
            "policy_type": "INVALID_POLICY_TYPE",
            "expiry_date": timezone.now().date().isoformat()
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 400)
        self.assertIn('policy_type', response.data)
        self.assertQuerySetEqual(Policy.objects.all(), [])

    def test_create_with_expiry_date_in_the_past(self):
        url = reverse("policies-list")
        data = {
            "customer_name": "Customer",
            "policy_type": Policy.Type.AUTO,
            "expiry_date": (timezone.now().date() - datetime.timedelta(days=1)).isoformat()
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 400)
        self.assertIn('expiry_date', response.data)
        self.assertQuerySetEqual(Policy.objects.all(), [])

    def test_create_valid_policy(self):
        url = reverse("policies-list")
        data = {
            "customer_name": "Customer",
            "policy_type": Policy.Type.AUTO,
            "expiry_date": timezone.now().date().isoformat()
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['customer_name'], data['customer_name'])
        self.assertEqual(response.data['policy_type'], data['policy_type'])
        self.assertEqual(response.data['expiry_date'], data['expiry_date'])
        self.assertEqual(response.data['policy_id'], 1)
        self.assertEqual(response.data['is_expired'], False)

    def test_delete_policy(self):
        create_policy(customer_name="Customer", policy_type=Policy.Type.AUTO)
        url = reverse("policies-detail", kwargs={ "pk": 1 })
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 204)
        self.assertQuerySetEqual(Policy.objects.all(), [])

    def test_patch_policy_with_date_in_the_past(self):
        create_policy(customer_name="Customer", policy_type=Policy.Type.AUTO)
        data = { "expiry_date": (timezone.now().date() - datetime.timedelta(days=1)).isoformat() }
        url = reverse("policies-detail", kwargs={ "pk": 1 })
        response = self.client.patch(url, data, "application/json")
        self.assertEqual(response.status_code, 400)
        self.assertIn('expiry_date', response.data)

    def test_patch_policy_with_date_in_the_future(self):
        create_policy(customer_name="Customer", policy_type=Policy.Type.AUTO)
        new_expiry_date = timezone.now().date() + datetime.timedelta(days=1)
        data = { "expiry_date": new_expiry_date.isoformat() }
        url = reverse("policies-detail", kwargs={ "pk": 1 })
        response = self.client.patch(url, data, "application/json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Policy.objects.get(pk=1).expiry_date, new_expiry_date)

    def test_detail_valid_policy(self):
        """
        The detail view of a valid policy should have the field is_expired set to False.
        """
        policy = create_policy(customer_name="Customer", policy_type=Policy.Type.AUTO)
        expected_content = PolicySerializer(instance=policy).data
        url = reverse("policies-detail", args=[policy.pk])
        response = self.client.get(url)
        self.assertFalse(expected_content.get('is_expired'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, expected_content)

    def test_detail_expired_policy(self):
        """
        The detail view of an expired policy should have the field is_expired set to True.
        """
        policy = create_policy(customer_name="Customer", policy_type=Policy.Type.AUTO, days_offset=-1)
        expected_content = PolicySerializer(instance=policy).data
        url = reverse("policies-detail", args=[policy.pk])
        response = self.client.get(url)
        self.assertTrue(expected_content.get('is_expired'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, expected_content)

    def test_detail_non_existent_policy(self):
        """
        The detail view of an invalid policy_id should return not found.
        """
        url = reverse("policies-detail", args=[1])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)
