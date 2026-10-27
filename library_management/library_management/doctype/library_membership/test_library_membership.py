# Copyright (c) 2026, Muthomi Newton and Contributors
# See license.txt

import frappe
from frappe.tests import IntegrationTestCase
from frappe.utils import getdate


class IntegrationTestLibraryMembership(IntegrationTestCase):
	def setUp(self):
		super().setUp()
		self.settings = frappe.get_single("Library Settings")
		self.settings.loan_period = 30
		self.settings.max_articles = 10
		self.settings.save()
		self.member = frappe.get_doc(
			{
				"doctype": "Library Member",
				"first_name": "Membership Test " + frappe.generate_hash(length=10),
			}
		).insert()

	def membership(self, start, member=None):
		return frappe.get_doc(
			{
				"doctype": "Library Membership",
				"library_member": member or self.member.name,
				"from_date": start,
			}
		)

	def test_end_date_is_available_on_draft(self):
		doc = self.membership("2026-01-01").insert()
		self.assertEqual(getdate(doc.to_date), getdate("2026-01-31"))

	def test_missing_start_date_is_rejected(self):
		with self.assertRaises(frappe.ValidationError):
			self.membership(None).insert()

	def test_shared_boundary_is_rejected(self):
		self.membership("2026-01-01").insert().submit()
		with self.assertRaises(frappe.ValidationError):
			self.membership("2026-01-31").insert().submit()

	def test_overlapping_period_is_rejected(self):
		self.membership("2026-01-01").insert().submit()
		with self.assertRaises(frappe.ValidationError):
			self.membership("2026-01-15").insert().submit()

	def test_next_day_renewal_is_allowed(self):
		self.membership("2026-01-01").insert().submit()
		doc = self.membership("2026-02-01").insert().submit()
		self.assertEqual(doc.docstatus, 1)

	def test_nonoverlapping_earlier_period_is_allowed(self):
		self.membership("2026-03-01").insert().submit()
		doc = self.membership("2026-01-01").insert().submit()
		self.assertEqual(doc.docstatus, 1)

	def test_draft_membership_does_not_block_submission(self):
		self.membership("2026-01-01").insert()
		doc = self.membership("2026-01-01").insert().submit()
		self.assertEqual(doc.docstatus, 1)

	def test_cancelled_membership_does_not_block_submission(self):
		self.membership("2026-01-01").insert().submit().cancel()
		doc = self.membership("2026-01-01").insert().submit()
		self.assertEqual(doc.docstatus, 1)

	def test_other_member_does_not_block_submission(self):
		self.membership("2026-01-01").insert().submit()
		other = frappe.get_doc(
			{
				"doctype": "Library Member",
				"first_name": "Other Member " + frappe.generate_hash(length=10),
			}
		).insert()
		doc = self.membership("2026-01-01", other.name).insert().submit()
		self.assertEqual(doc.docstatus, 1)

	def test_invalid_settings_are_rejected(self):
		for field in ("loan_period", "max_articles"):
			for value in (0, -1):
				with self.subTest(field=field, value=value):
					settings = frappe.get_single("Library Settings")
					settings.set(field, value)
					with self.assertRaises(frappe.ValidationError):
						settings.save()
