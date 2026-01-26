# -*- coding: utf-8 -*-

from odoo import api, fields, models
from odoo.exceptions import ValidationError


class StudentAttendance(models.Model):
    _name = "edu.student.attendance"
    _description = "Student Attendance"
    _order = "attendance_date desc, student_id"

    attendance_date = fields.Date(required=True, index=True)
    status = fields.Selection(
        [
            ("present", "Present"),
            ("absent", "Absent"),
            ("late", "Late"),
        ],
        required=True,
        default="present",
        index=True,
    )
    student_id = fields.Many2one(
        "edu.student",
        required=True,
        ondelete="cascade",
        index=True,
    )
    class_id = fields.Many2one(
        "edu.academic.class",
        string="Class",
        required=True,
        ondelete="restrict",
        index=True,
    )
    section_id = fields.Many2one(
        "edu.academic.section",
        string="Section",
        ondelete="restrict",
        index=True,
    )
    note = fields.Text()
    company_id = fields.Many2one(
        "res.company",
        related="student_id.company_id",
        store=True,
        readonly=True,
        index=True,
    )

    _sql_constraints = [
        (
            "student_attendance_unique",
            "unique(student_id, attendance_date)",
            "A student can only have one attendance record per date.",
        )
    ]

    @api.constrains("class_id", "section_id")
    def _check_section_class(self):
        for record in self:
            if (
                record.section_id
                and record.class_id
                and record.section_id.class_id != record.class_id
            ):
                raise ValidationError("Section must belong to the selected class.")
