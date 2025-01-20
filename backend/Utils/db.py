from prisma import Prisma
from prisma.errors import PrismaError, UniqueViolationError

# Global database instance
_db = None


async def init_db():
    """Initialize the database connection."""
    global _db
    try:
        _db = Prisma()
        await _db.connect()
    except PrismaError as e:
        print(f"Error connecting to database: {e}")
        raise


async def close_db():
    """Close the database connection."""
    global _db
    if _db:
        try:
            await _db.disconnect()
            _db = None
        except PrismaError as e:
            print(f"Error disconnecting from database: {e}")
            raise


async def get_db():
    """Get database client."""
    try:
        global _db
        if not _db:
            await init_db()
        return _db
    except Exception as e:
        print(f"Database operation failed: {e}")
        raise


async def get_all_records():
    try:
        db = await get_db()
        records = await db.statement.find_many(
            include={
                'total_total': {
                    "include": {
                        'securities': True
                    }
                },
                'realized_total': {
                    "include": {
                        'securities': True
                    }
                },
                'unrealized_total': {
                    "include": {
                        'securities': True
                    }
                },
            }
        )
        return records
    except Exception as e:
        print(f"Error while getting all records in database: {e}")
        raise


async def add_new_statement(data):
    db = await get_db()
    try:
        record = await db.statement.create(data)
        return record
    except UniqueViolationError as e:
        print(f"Statement record already exists. You may be trying to\n"
              f"scan an old statement")
    except PrismaError as e:
        print(f"Error creating new account: {e}")
        raise


async def statement_exists(data):
    db = await get_db()
    try:
        record = await db.statement.find_unique(
            where={
                'statementdate_account': {
                    'statement_start': data['statement_start'],
                    'statement_end': data['statement_end'],
                    'account_name': data['account_name'],
                }
            }
        )
        return record is not None
    except PrismaError as e:
        print(f"Error while checking if statement exists: {e}")
        raise


async def add_new_total_total(data):
    try:
        db = await get_db()
        record = await db.totaltotal.create(data)
        return record
    except UniqueViolationError as e:
        print(f"TotalTotal record already exists. You may be trying to scan an old statement.")
    except PrismaError as e:
        print(f"Error adding new total: {e}")
        raise


async def add_new_realized_total(data):
    try:
        db = await get_db()
        record = await db.realizedtotal.create(data)
        return record
    except UniqueViolationError as e:
        print(f"RealizedTotal record already exists. You may be trying to scan an old statement.")
    except PrismaError as e:
        print(f"Error adding new realized total: {e}")
        raise


async def add_new_unrealized_total(data):
    try:
        db = await get_db()
        record = await db.unrealizedtotal.create(data)
        return record
    except UniqueViolationError as e:
        print(f"UnrealizedTotal record already exists. You may be trying to scan an old statement.")
    except PrismaError as e:
        print(f"Error adding new unrealized total: {e}")
        raise


async def add_new_securities(data):
    try:
        db = await get_db()
        record = await db.security.create_many(data)
        return record
    except UniqueViolationError as e:
        print(f"Security record already exists. You may be trying to scan an old statement.")
    except PrismaError as e:
        print(f"Error creating new security: {e}")
        raise
