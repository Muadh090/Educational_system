# -*- coding: utf-8 -*-

from odoo import api, fields, models


class EduDashboard(models.Model):
    _name = "edu.dashboard"
    _description = "Education Dashboard"

    name = fields.Char(required=True, default="Dashboard")
    students_count = fields.Integer(compute="_compute_kpis")
    teachers_count = fields.Integer(compute="_compute_kpis")
    attendance_count = fields.Integer(compute="_compute_kpis")
    fees_amount_total = fields.Monetary(compute="_compute_kpis")
    currency_id = fields.Many2one(
        "res.currency",
        default=lambda self: self.env.company.currency_id,
        required=True,
    )
    company_id = fields.Many2one(
        "res.company",
        default=lambda self: self.env.company,
        required=True,
        index=True,
    )

    @api.depends("company_id")
    def _compute_kpis(self):
        today = fields.Date.context_today(self)
        for record in self:
            company_domain = [("company_id", "=", record.company_id.id)]
            record.students_count = self.env["edu.student"].search_count(company_domain)
            record.teachers_count = self.env["edu.teacher"].search_count(company_domain)
            record.attendance_count = self.env["edu.student.attendance"].search_count(
                company_domain + [("attendance_date", "=", today)]
            )
            fees_group = self.env["edu.student.invoice"].read_group(
                company_domain,
                ["amount_total:sum"],
                [],
            )
            record.fees_amount_total = fees_group[0]["amount_total"] if fees_group else 0.0
