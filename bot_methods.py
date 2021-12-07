from enum import Enum, auto
from bot_internals import *


def load():
    load_data()


def save_info():
    save_data()


def view():
    print(guild_dict)


def user_has_bot_permissions(user):
    return user_has_roles(["admin", "asistente"], user)


#  gets global_course parameter to make explicit call
def add_course_to_guild(code, global_course=False, guild='global'):
    code = code.upper()
    if global_course:
        guild_id = guild
    else:
        guild_id = guild_bot_id(guild)
    validate_guild_in_dict(guild_id)
    for dic in guild_dict[guild_id]['courses']:
        if code in dic:
            return False
    guild_dict[guild_id]['courses'].append({str(code): [], "done": []})
    save_info()
    return True


class AddStudentResult(Enum):
    SUCCESS = auto()
    NO_COURSE = auto()
    REPEATED_ID = auto()

# def add_student_to_course(student_id, course_code, guild):
#     result = add_student_to_course_in_guild(student_id, course_code, guild)
#     if result is AddStudentResult.NO_COURSE:
#         return add_student_to_global_course(student_id, course_code)
#     else:
#         return result


def add_student_to_course(student_id, course_code, guild):
    course_code = course_code.upper()
    guild_id = 'global'
    validate_guild_in_dict(guild_id)
    for course in guild_dict[guild_id]['courses']:
        if course_code in course:
            if student_id in course[course_code]:
                return AddStudentResult.REPEATED_ID
            course[course_code].append(f'{student_id}-{guild.name}')
            course['done'].append(False)
            save_info()
            return AddStudentResult.SUCCESS
    return AddStudentResult.NO_COURSE


def add_student_to_global_course(student_id, course_code):
    """This function should only be used internally in bot_methods.py
        It looks for a course in the global list and adds the student_id
        to the list
    """
    course_code = course_code.upper()
    validate_guild_in_dict('global')
    for course in guild_dict['global']['courses']:
        if course_code in course:
            if student_id in course[course_code]:
                return AddStudentResult.REPEATED_ID
            course[course_code].append(student_id)
            save_info()
            return AddStudentResult.SUCCESS
    return AddStudentResult.NO_COURSE


class MarkStudentDoneResult(Enum):
    SUCCESS = auto()
    NO_COURSE = auto()
    NO_STUDENT = auto()


def mark_student_as_done_in_course(student_id, course_code):
    course_code = course_code.upper()
    guild_id = 'global'
    validate_guild_in_dict(guild_id)
    for course in guild_dict[guild_id]['courses']:
        if course_code in course:
            for i, student in enumerate(course[course_code]):
                if student_id in student:
                    course['done'][i] = True
                    return MarkStudentDoneResult.SUCCESS
            return MarkStudentDoneResult.NO_STUDENT
    return MarkStudentDoneResult.NO_COURSE


def remove_student_from_course(student_id, course_code):
    course_code = course_code.upper()
    guild_id = 'global'
    validate_guild_in_dict(guild_id)
    for course in guild_dict[guild_id]['courses']:
        if course_code in course:
            for i, student in enumerate(course[course_code]):
                if student_id in student:
                    course[course_code].remove(student)
                    course['done'].pop(i)
                    save_info()


class GetWaitlistResult(Enum):
    SUCCESS = auto()
    NO_COURSE = auto()


def get_course_waitlist(course_code):
    course_code = course_code.upper()
    for guild in guild_dict:
        for course in guild_dict[guild]['courses']:
            if course_code in course:
                return course[course_code], GetWaitlistResult.SUCCESS
    return [], GetWaitlistResult.NO_COURSE


def add_to_queue_in_guild(user, guild):
    guild_id = guild_bot_id(guild)
    validate_guild_in_dict(guild_id)
    if user in queue_dict[guild_id]:
        return False
    queue_dict[guild_id].append(user)
    return True


def leave_from_queue_in_guild(user, guild):
    guild_id = guild_bot_id(guild)
    validate_guild_in_dict(guild_id)
    if user in queue_dict[guild_id]:
        queue_dict[guild_id].remove(user)


def get_next_from_queue_in_guild(assistant, guild):
    guild_id = guild_bot_id(guild)
    validate_guild_in_dict(guild_id)
    next_user = queue_dict[guild_id][0]
    queue_dict[guild_id].remove(next_user)
    return next_user


def get_guild_queue(guild):
    """ Use this as read-only
    """
    guild_id = guild_bot_id(guild)
    validate_guild_in_dict(guild_id)
    return queue_dict[guild_id]


def eraseQueue(guild):
    g = guild_bot_id(guild)
    queue_dict[g].clear()
