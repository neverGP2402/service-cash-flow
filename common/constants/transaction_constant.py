class TransactionType:
    INCOME = 'INCOME'
    EXPENSE = 'EXPENSE'


class TransactionStatus:
    PENDING = 'PENDING'
    COMPLETED = 'COMPLETED'
    FAILED = 'FAILED'


class FormalityTransaction:
    CASH = 'CASH'
    BANK = 'BANK'
    OTHER = 'OTHER'


class NotificationType:
    REMIND = 'remind'
    WARNING = 'warning'
    NOTIFY = 'notify'


class PriorityType:
    LOW = 'low'
    MEDIUM = 'medium'
    HIGH = 'high'
