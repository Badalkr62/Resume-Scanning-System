from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    Image,
    HRFlowable,
)

from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.enums import TA_CENTER

from django.conf import settings
from accounts.models import UserProfile

import os
import random


def generate_offer_letter(application):

    # ==========================
    # Create Folder
    # ==========================

    folder = os.path.join(settings.MEDIA_ROOT, "offer_letters")
    os.makedirs(folder, exist_ok=True)

    filename = f"Offer_{application.user.username}.pdf"
    pdf_path = os.path.join(folder, filename)

    offer_no = f"ATS-{random.randint(10000, 99999)}"

    # ==========================
    # Candidate Profile
    # ==========================

    profile = UserProfile.objects.filter(
        user=application.user
    ).first()

    phone = "Not Available"

    if profile and profile.phone:
        phone = profile.phone

    # ==========================
    # Images
    # ==========================

    logo_path = os.path.join(
        settings.MEDIA_ROOT,
        "company",
        "logo.png",
    )

    stamp_path = os.path.join(
        settings.MEDIA_ROOT,
        "company",
        "stamp.png",
    )

    signatures = [
        "hr_signature.png",
        "hr_signature1.png",
        "hr_signature2.png",
        "hr_signature3.png",
    ]

    signature_path = os.path.join(
        settings.MEDIA_ROOT,
        "company",
        random.choice(signatures),
    )

    # ==========================
    # PDF
    # ==========================

    doc = SimpleDocTemplate(pdf_path)

    styles = getSampleStyleSheet()

    title = styles["Heading1"]
    title.alignment = TA_CENTER

    heading = styles["Heading2"]
    heading.alignment = TA_CENTER

    normal = styles["BodyText"]

    story = []

    # ==========================
    # Logo
    # ==========================

    if os.path.exists(logo_path):
        story.append(Image(logo_path, width=90, height=90))

    story.append(Paragraph("SMART RESUME ATS", title))
    story.append(Paragraph("HR Department", heading))

    story.append(Spacer(1, 8))

    story.append(
        Paragraph(
            "Smart Recruiter Technologies Pvt. Ltd.<br/>"
            "Hazaribagh, Jharkhand - 825301<br/>"
            "www.smartresumeats.com",
            normal,
        )
    )

    story.append(Spacer(1, 10))

    story.append(HRFlowable(width="100%"))

    story.append(Spacer(1, 20))

    story.append(
        Paragraph(
            "<b>OFFICIAL OFFER LETTER</b>",
            heading,
        )
    )

    story.append(Spacer(1, 20))

    story.append(
        Paragraph(
            "Date : 06 July 2026",
            normal,
        )
    )

    story.append(Spacer(1, 15))

    story.append(
        Paragraph(
            f"Dear <b>{application.user.get_full_name() or application.user.username}</b>,",
            normal,
        )
    )

    story.append(Spacer(1, 12))

    story.append(
        Paragraph(
            "Congratulations! We are delighted to offer you employment with SMART RESUME ATS. "
            "Based on your interview performance, we are pleased to appoint you to the following position.",
            normal,
        )
    )

    story.append(Spacer(1, 20))

    # ==========================
    # Candidate Details
    # ==========================

    story.append(
        Paragraph(
            f"<b>Offer No :</b> {offer_no}",
            normal,
        )
    )

    story.append(
        Paragraph(
            f"<b>Candidate Name :</b> {application.user.get_full_name() or application.user.username}",
            normal,
        )
    )
    story.append(
        Paragraph(
            f"<b>Mobile :</b> {phone}",
            normal,
        )
    )

    story.append(
        Paragraph(
            f"<b>Email :</b> {application.user.email}",
            normal,
        )
    )

    story.append(
        Paragraph(
            f"<b>Candidate ID :</b> ATS-{application.user.id}",
            normal,
        )
    )

    story.append(Spacer(1, 20))

    # ==========================
    # Job Table
    # ==========================

    data = [

        ["Position", application.job.title],

        ["Company", application.job.company],

        ["Department", "Software Development"],

        ["Location", application.job.location],

        ["Salary", str(application.job.salary)],

        ["Joining Date", "15 July 2026"],

    ]

    table = Table(
        data,
        colWidths=[180, 250],
    )

    table.setStyle(

        TableStyle(

            [

                ("GRID", (0, 0), (-1, -1), 1, colors.black),

                ("BACKGROUND", (0, 0), (0, -1), colors.lightgrey),

                ("FONTNAME", (0, 0), (-1, -1), "Helvetica"),

                ("BOTTOMPADDING", (0, 0), (-1, -1), 10),

            ]

        )

    )

    story.append(table)

    story.append(Spacer(1, 25))

    # ==========================
    # Terms
    # ==========================

    story.append(Paragraph("<b>Terms & Conditions</b>", heading))

    terms = [

        "1. You will report to the HR Department on your joining date.",

        "2. Bring all original educational documents.",

        "3. Employment is subject to company policies.",

        "4. Company reserves the right to terminate employment as per company policy.",

    ]

    for term in terms:
        story.append(
            Paragraph(term, normal)
        )

    story.append(Spacer(1, 35))

    story.append(
        Paragraph(
            "We look forward to welcoming you to our team.",
            normal,
        )
    )

    story.append(Spacer(1, 25))

    # ==========================
    # Signature
    # ==========================

    if os.path.exists(signature_path):
        story.append(
            Image(
                signature_path,
                width=130,
                height=50,
            )
        )

    story.append(
        Paragraph(
            "<b>HR Manager</b>",
            normal,
        )
    )

    story.append(
        Paragraph(
            "SMART RESUME ATS",
            normal,
        )
    )

    # ==========================
    # Stamp
    # ==========================

    if os.path.exists(stamp_path):
        story.append(Spacer(1, 10))
        story.append(
            Image(
                stamp_path,
                width=80,
                height=80,
            )
        )

    doc.build(story)

    return pdf_path
