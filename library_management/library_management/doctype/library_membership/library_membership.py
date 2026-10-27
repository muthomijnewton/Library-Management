# Copyright (c) 2026, Muthomi Newton and contributors
# For license information, please see license.txt

import frappe
from frappe.model.docstatus import DocStatus
from frappe.model.document import Document
from frappe.utils import add_days, cint


class LibraryMembership(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		amended_from: DF.Link | None
		from_date: DF.Date | None
		full_name: DF.Data | None
		library_member: DF.Link
		paid: DF.Check
		to_date: DF.Date | None
	# end: auto-generated types

	_DOCTYPE_NAME = "Library Membership"

	def validate(self):
		if not self.from_date:
			frappe.throw("From Date is required")

		loan_period = frappe.db.get_single_value("Library Settings", "loan_period")
		# Preserve the existing 30-day fallback for unconfigured sites.
		loan_period = 30 if loan_period in (None, "") else cint(loan_period)
		if loan_period <= 0:
			frappe.throw("Loan Period must be greater than zero")
		self.to_date = add_days(self.from_date, loan_period)

	def before_submit(self):
		# Borrowing eligibility includes both endpoints, so overlap must too.
		exists = frappe.db.exists(
			"Library Membership",
			{
				"library_member": self.library_member,
				"docstatus": DocStatus.submitted(),
				"from_date": ("<=", self.to_date),
				"to_date": (">=", self.from_date),
				"name": ("!=", self.name),
			},
		)
		if exists:
			frappe.throw("There is an overlapping membership for this member")
