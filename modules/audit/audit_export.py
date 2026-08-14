
"""
GeoMaka POS Audit Log Export

File:
modules/audit/audit_export.py

Purpose:
Export GeoMaka POS audit logs to a text report.

Responsibilities:

- Create the audit export directory.
- Format audit log records.
- Generate readable audit reports.
- Save audit reports as text files.
- Use YYYY-MM-DD for audit report filenames.
- Record successful audit report exports.
- Handle empty audit logs safely.
- Never fail an audit report export because of
  an audit logging failure.

Company:
GeoMaka Technologies
"""

from datetime import datetime


from modules.system.app_paths import (
    get_audit_directory
)


from modules.audit.audit_logs import (
    log_activity
)


# ==========================================================
# SAVE TEXT FILE
# ==========================================================

def _save_text_file(
    filename,
    content
):
    """
    Saves audit report content to the audit directory.

    Parameters:

        filename:
            Name of the file to create.

        content:
            Text content to save.

    Returns:

        Path to the saved file.

    Raises:

        OSError:
            If the directory or file cannot be created.
    """

    # ======================================================
    # GET AUDIT DIRECTORY
    # ======================================================

    audit_directory = (
        get_audit_directory()
    )


    # ======================================================
    # CREATE AUDIT DIRECTORY
    # ======================================================

    audit_directory.mkdir(
        parents=True,
        exist_ok=True
    )


    # ======================================================
    # BUILD FILE PATH
    # ======================================================

    file_path = (
        audit_directory
        /
        filename
    )


    # ======================================================
    # SAVE FILE
    # ======================================================

    with open(
        file_path,
        "w",
        encoding="utf-8"
    ) as file:

        file.write(
            content
        )


    return file_path


# ==========================================================
# FORMAT TABLE VALUE
# ==========================================================

def _format_table_value(
    value,
    width
):
    """
    Converts a value to text and formats it to fit
    the specified table column width.

    Long values are truncated so that the audit report
    remains readable and aligned.
    """

    if value is None:

        value = ""

    else:

        value = str(
            value
        )


    # ======================================================
    # TRUNCATE LONG VALUE
    # ======================================================

    if len(value) > width:

        if width > 3:

            value = (
                value[:width - 3]
                +
                "..."
            )

        else:

            value = value[:width]


    # ======================================================
    # ALIGN VALUE
    # ======================================================

    return value.ljust(
        width
    )


# ==========================================================
# AUDIT TABLE FORMATTER
# ==========================================================

def _format_audit_table(
    logs
):
    """
    Formats audit log records into a readable text table.

    Expected log fields:

        log_datetime
        username
        role
        module
        action
        description
    """

    # ======================================================
    # COLUMN WIDTHS
    # ======================================================

    date_width = 20

    username_width = 15

    role_width = 15

    module_width = 15

    action_width = 15

    description_width = 40


    table_width = (
        date_width
        +
        username_width
        +
        role_width
        +
        module_width
        +
        action_width
        +
        description_width
    )


    text = ""


    # ======================================================
    # TOP BORDER
    # ======================================================

    text += (
        "-"
        *
        table_width
        +
        "\n"
    )


    # ======================================================
    # TABLE HEADER
    # ======================================================

    text += (
        _format_table_value(
            "Date & Time",
            date_width
        )
        +
        _format_table_value(
            "Username",
            username_width
        )
        +
        _format_table_value(
            "Role",
            role_width
        )
        +
        _format_table_value(
            "Module",
            module_width
        )
        +
        _format_table_value(
            "Action",
            action_width
        )
        +
        _format_table_value(
            "Description",
            description_width
        )
        +
        "\n"
    )


    # ======================================================
    # HEADER SEPARATOR
    # ======================================================

    text += (
        "-"
        *
        table_width
        +
        "\n"
    )


    # ======================================================
    # CHECK EMPTY LOGS
    # ======================================================

    if not logs:

        empty_text = (
            "No audit log records found."
        )


        text += (
            _format_table_value(
                empty_text,
                table_width
            )
            +
            "\n"
        )


    # ======================================================
    # ADD LOG RECORDS
    # ======================================================

    else:

        for log in logs:

            # --------------------------------------------------
            # SUPPORT DICTIONARY-STYLE DATABASE ROWS
            # --------------------------------------------------

            try:

                log_datetime = (
                    log["log_datetime"]
                )

                username = (
                    log["username"]
                )

                role = (
                    log["role"]
                )

                module = (
                    log["module"]
                )

                action = (
                    log["action"]
                )

                description = (
                    log["description"]
                )


            except (
                TypeError,
                KeyError
            ):

                # --------------------------------------------------
                # SUPPORT TUPLE-STYLE ROWS
                #
                # Expected tuple:
                #
                # (
                #     audit_id,
                #     log_datetime,
                #     username,
                #     role,
                #     module,
                #     action,
                #     description
                # )
                # --------------------------------------------------

                try:

                    (
                        _audit_id,
                        log_datetime,
                        username,
                        role,
                        module,
                        action,
                        description
                    ) = log


                except (
                    TypeError,
                    ValueError
                ):

                    continue


            # --------------------------------------------------
            # FORMAT DATE/TIME
            # --------------------------------------------------

            if isinstance(
                log_datetime,
                datetime
            ):

                log_datetime = (
                    log_datetime.strftime(
                        "%Y-%m-%d %H:%M:%S"
                    )
                )

            else:

                log_datetime = str(
                    log_datetime
                )


            # --------------------------------------------------
            # FORMAT RECORD
            # --------------------------------------------------

            text += (
                _format_table_value(
                    log_datetime,
                    date_width
                )
                +
                _format_table_value(
                    username,
                    username_width
                )
                +
                _format_table_value(
                    role,
                    role_width
                )
                +
                _format_table_value(
                    module,
                    module_width
                )
                +
                _format_table_value(
                    action,
                    action_width
                )
                +
                _format_table_value(
                    description,
                    description_width
                )
                +
                "\n"
            )


    # ======================================================
    # BOTTOM BORDER
    # ======================================================

    text += (
        "-"
        *
        table_width
        +
        "\n"
    )


    return text


# ==========================================================
# SAVE AUDIT LOG REPORT
# ==========================================================

def save_audit_logs_report(
    generated,
    logs
):
    """
    Creates and saves an audit log report.

    Parameters:

        generated:
            Date/time when the report was generated.

        logs:
            Audit log records to export.

    Returns:

        Path to the saved audit report.

    Raises:

        OSError:
            If the report cannot be saved.
    """

    # ======================================================
    # REPORT HEADER
    # ======================================================

    content = ""


    content += (
        "="
        *
        130
        +
        "\n"
    )


    content += (
        " "
        *
        50
        +
        "AUDIT LOG REPORT\n"
    )


    content += (
        "="
        *
        130
        +
        "\n\n"
    )


    # ======================================================
    # REPORT INFORMATION
    # ======================================================

    content += (
        f"Generated : {generated}\n"
    )


    content += (
        f"Total Records : {len(logs)}\n\n"
    )


    # ======================================================
    # AUDIT TABLE
    # ======================================================

    content += _format_audit_table(
        logs
    )


    content += "\n"


    # ======================================================
    # REPORT FOOTER
    # ======================================================

    content += (
        "="
        *
        130
        +
        "\n"
    )


    content += (
        "Generated by GeoMaka POS\n"
    )


    content += (
        "GeoMaka Technologies\n"
    )


    content += (
        "="
        *
        130
    )


    # ======================================================
    # CREATE DATE-BASED FILENAME
    # ======================================================
    #
    # Required format:
    #
    # YYYY-MM-DD
    #
    # Example:
    #
    # audit_logs_2026-08-13.txt
    #
    # ======================================================

    file_date = datetime.now().strftime(
        "%Y-%m-%d"
    )


    filename = (
        f"audit_logs_{file_date}.txt"
    )


    # ======================================================
    # SAVE REPORT
    # ======================================================

    file_path = _save_text_file(
        filename,
        content
    )


    # ======================================================
    # AUDIT SUCCESSFUL EXPORT
    # ======================================================
    #
    # The file has already been saved successfully.
    #
    # Therefore an audit logging failure must NOT
    # cause this export operation to fail.
    #
    # Short description:
    #
    # Audit report exported
    #
    # ======================================================

    try:

        log_activity(
            module="AUDIT",
            action="EXPORT",
            description="Audit report exported"
        )

    except Exception:

        pass


    # ======================================================
    # RETURN SAVED FILE
    # ======================================================

    return file_path

