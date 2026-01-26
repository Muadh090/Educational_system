# -*- coding: utf-8 -*-

from odoo import fields, models


class Exam(models.Model):
    _name = "edu.exam"
    _description = "Exam"
    _order = "date desc"

    name = fields.Char(required=True, index=True)
    code = fields.Char(index=True)
    date = fields.Date(required=True, index=True)
    active = fields.Boolean(default=True)

    academic_year_id = fields.Many2one(
        "edu.academic.year",
        ondelete="restrict",
        index=True,
    )
    term_id = fields.Many2one(
        "edu.academic.term",
        ondelete="restrict",
        index=True,
    )
    class_id = fields.Many2one(
        "edu.academic.class",
        string="Class",
        ondelete="restrict",
        index=True,
    )
    subject_id = fields.Many2one(
        "edu.academic.subject",
        string="Subject",
        ondelete="restrict",
        index=True,
    )

    ca_ids = fields.One2many(
        "edu.continuous.assessment",
        "exam_id",
        string="Continuous Assessments",
    )

    company_id = fields.Many2one(
        "res.company",
        default=lambda self: self.env.company,
        required=True,
        index=True,
    )

    _sql_constraints = [
        (
            "exam_name_company_uniq",
            "unique(name, company_id)",
            "The exam name must be unique per company.",
        )
    ]
