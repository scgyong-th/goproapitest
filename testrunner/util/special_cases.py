# excludes.

from camera import SettingId, StatusId
from types import SimpleNamespace

cases = SimpleNamespace()
cases.settings = SimpleNamespace()
cases.settings.excludes = {
    'ENABLE_NIGHT_PHOTO',
    'MAX_LENS',
    'MULTI_SHOT_DURATION',
    'VIDEO_PERFORMANCE_MODE',
}
cases.statuses = SimpleNamespace()
cases.statuses.excludes = {
    'CLIENT_WIFI_NAME',
    'IS_FIRST_TIME_USE',
    'IS_MOBILE_FRIENDLY',
    'LAST_PAIRING_TIME_MS',
    'LENS_TYPE',
    'LINUX_CORE_ACTIVE',
    'LIVE_BURST_REMAINING',
    'PREVIEW_STREAM_ENABLED',
    'TOTAL_LIVE_BURSTS',
    'WIRELESS_PAIRING_STATE',
    'WIRELESS_REMOTE_VERSION',
}
