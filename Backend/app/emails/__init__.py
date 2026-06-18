"""
The Email Package responsible for composing and sending application emails.

This package centralizes email-specific logic, including template rendering,
subject construction, and delivery through the configured email provider.

It is kept separate from the database service layer to preserve a clear
architectural boundary: database-related operations belong in services,
while outbound email functionality belongs in this package.

Routes may call functions from this package directly when email sending is
part of the route workflow.
"""