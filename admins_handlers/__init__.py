from .add_admin_cmd import add_admin_router, add_admin_cmd, cancel_adding_cmd, get_new_admin_id
from .delete_admin_cmd import delete_admin_router, delete_admin_cmd, cancel_admin_deleting, get_id_to_delete_admin
from .ads_send_cmd import (ads_send_router, send_cmd, get_ads_text, get_confirm_callback, send_without_photo_callback,
                           send_with_photo_callback, get_photo, confirm_photo, send_ads_without_button, add_button,
                           get_btn_text, get_btn_link, confirm_button, cmd_cancel_ads_sending)

print("INIT admins_handlers")
