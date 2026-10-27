# Copyright (c) 2026, Muthomi Newton and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import cint


class LibrarySettings(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		loan_period: DF.Int
		max_articles: DF.Int
	# end: auto-generated types

	_DOCTYPE_NAME = "Library Settings"

	def validate(self):
		if cint(self.loan_period) <= 0:
			frappe.throw(_("Loan Period must be greater than zero"))
		if cint(self.max_articles) <= 0:
			frappe.throw(_("Maximum Number of Issued Articles must be greater than zero"))
