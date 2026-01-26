# -*- coding: utf-8 -*-

from odoo import fields, models


class ELearningMaterial(models.Model):
    _name = "edu.elearning.material"
    _description = "E-learning Material"
    _order = "publish_date desc, id desc"

    name = fields.Char(required=True, index=True)
    description = fields.Html()
    publish_date = fields.Date(index=True)

    teacher_id = fields.Many2one(
        "edu.teacher",
        required=True,
        ondelete="restrict",
        index=True,
    )
    class_id = fields.Many2one(
        "edu.academic.class",
        string="Class",
        ondelete="restrict",
        index=True,
    )
    section_id = fields.Many2one(
        "edu.academic.section",
        string="Section",
        ondelete="restrict",
        index=True,
    )
    subject_id = fields.Many2one(
        "edu.academic.subject",
        string="Subject",
        ondelete="restrict",
        index=True,
    )

    student_ids = fields.Many2many(
        "edu.student",
        "edu_material_student_rel",
        "material_id",
        "student_id",
        string="Available To",
    )

    attachment_ids = fields.Many2many(
        "ir.attachment",
        "edu_material_attachment_rel",
        "material_id",
        "attachment_id",
        string="Attachments",
    )

    active = fields.Boolean(default=True)
    company_id = fields.Many2one(
        "res.company",
        default=lambda self: self.env.company,
        required=True,
        index=True,
    )
