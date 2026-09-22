# Copyright (c) 2026, Muthomi Newton and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document
from frappe.model.docstatus import DocStatus


class LibraryTransaction(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		amended_from: DF.Link | None
		article: DF.Link
		date: DF.Date
		library_member: DF.Link
		type: DF.Literal["Issue", "Return"]
	# end: auto-generated types

	_DOCTYPE_NAME = "Library Transaction"

	def before_save(self):
		if self.type == "Issue":
			self.validate_issue()

			article = frappe.get_doc("Article", self.article)
			article.status("Issued")
			article.save()

		elif self.type == "Return":
			self.validate_return()

			article = frappe.get_doc("Article", self.article)
			article.status("Available")
			article.save()


	def validate_issue(self):
		self.validate_membership()
		article = frappe.get_doc("Article", self.article)

		if article.status == "Issued":
			frappe.throw("Article is already issued by another member")

	def validate_return(self):
		article = frappe.get_doc("Article", self.article)

		if article.status == "Available":
			frappe.throw("Article cannot be returned without being issued first")

	def validate_maximum_limit(self):
		max_articles = frappe.db.get_single_value("Library Settings", "max_articles")
		count = frappe.db.count(
			"Library Transaction",
			{
				"library_member":self.library_member,
				"type": "Issue",
				"docstatus": DocStatus.submitted(),
			},
		)
		if count >= max_articles:
			frappe.throw("Maximum limit reached for issuing articles")

	def validate_membership(self):
		valid_membership = frappe.db.exists(
			"Library Membership",
			{
				"library_member": self.library_member,
				"docstatus": DocStatus.submitted(),
				"from_date": ("<", self.date),
				"to_date": (">", self.date),
			},
		)

		if not valid_membership:
			frappe.throw("The member does not have a valid membership")

