"""
Docstring for Backend.app.constants.message_and_thread
"""
from enum import Enum

# class ThreadEventType(str, Enum): 
#     STATUS_CHANGED = "STATUS_CHANGED"
#     FLAG_CHANGED = "FLAG_CHANGED"
#     MARKED_SPAM = "MARKED_SPAM"
#     MARKED_ANSWER_NEEDED = "MARKED_ANSWER_NEEDED"
#     ASSIGNED = "ASSIGNED"
#     PRIORITY_CHANGED = "PRIORITY_CHANGED"

class ThreadStatus(str, Enum): # visible to user!!
    NEW = "NEW"
    OPEN = "OPEN"
    WAITING_ON_SUPPORT = "WAITING_ON_SUPPORT"
    WAITING_ON_CUSTOMER = "WAITING_ON_CUSTOMER"
    CLOSED = "CLOSED"
    UNDER_REVIEW = "UNDER_REVIEW" # use this to softly 'mark as spam'

class ThreadPriority(str, Enum):
    LOW = "LOW"
    NORMAL = "NORMAL"
    HIGH = "HIGH"
    URGENT = "URGENT"

THREAD_PRIORITY_SCORE = {
    ThreadPriority.LOW: 1,
    ThreadPriority.NORMAL: 2,
    ThreadPriority.HIGH: 3,
    ThreadPriority.URGENT: 4,
}
class MessageDirection(str, Enum):
    INBOUND = "INBOUND"     # from user/visitor to you
    OUTBOUND = "OUTBOUND"   # from admin/support to user

class MessageChannel(str, Enum):
    CONTACT_FORM = "CONTACT_FORM"
    USER_TO_SUPPORT = "USER_TO_SUPPORT"
    STAFF_TO_USER = "STAFF_TO_USER" #eg: admin sends message to user
    # SYSTEM_TO_USER = "SYSTEM_TO_USER"

