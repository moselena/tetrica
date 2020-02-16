with open('lessons.txt', 'r', encoding='utf-8') as f:
    data = f.read().split('\n')

with open('participants.txt', 'r', encoding='utf-8') as f:
    participants = f.read().split('\n')

with open('users.txt', 'r', encoding='utf-8') as f:
    users = f.read().split('\n')

with open('quality.txt', 'r', encoding='utf-8') as f:
    quality = f.read().split('\n')


def prepare_users(user):
    prepared = user.replace(' ', '').split('|')
    prepared = {'id': prepared[0], 'role': prepared[1]}

    return prepared


def prepare_participants(participant):
    prepared = participant.replace(' ', '').split('|')
    prepared = {'event_id': prepared[0], 'user_id': prepared[1]}

    return prepared


def prepare_lessons(lesson):
    prepared = lesson.replace(' ', '').split('|')
    prepared[3] = prepared[3][:10] + ' ' + prepared[3][10:]
    prepared = {'id': prepared[0], 'event_id': prepared[1], 'subject': prepared[2], 'scheduled_time': prepared[3]}

    return prepared


def prepare_quality(quality):
    prepared = quality.replace(' ', '').split('|')
    prepared = {'lesson_id': prepared[0], 'tech_quality': prepared[1]}

    return prepared


participants = list(map(prepare_participants, participants))
lessons = list(map(prepare_lessons, data))
users = list(map(prepare_users, users))
quality = list(map(prepare_quality, quality))

phys_lessons = [x for x in lessons if x['subject'] == 'phys']

days = {}

for event in phys_lessons:
    event_date = event['scheduled_time'].split(' ')[0]
    if event_date in days:
        days[event_date]['list'].append(event)
    else:
        days[event_date] = {
            'list': [event],
        }


def map_event(event):
    event['participants'] = []
    event['quality'] = []
    for participant in participants:
        if participant['event_id'] == event['event_id'] and not participant['user_id'] in event['participants']:
            event['participants'].append(participant['user_id'])

    for user in users:
        if user['id'] in event['participants']:
            participant_index = event['participants'].index(user['id'])
            event['participants'][participant_index] = user

    for mark in quality:
        if mark['lesson_id'] == event['id'] and mark['tech_quality'] != '':
            if (len(event['quality']) > 0):
                event_mark = event['quality'][0]
                event['quality'][0] = (event_mark + int(mark['tech_quality'])) / 2
            else:
                event['quality'].append(int(mark['tech_quality']))

    return event


for date, events in days.items():
    day_events = events['list']
    for event in day_events:
        event = map_event(event)

for date, events in days.items():
    tutors = []
    tutors_with_quality = []
    for event in events['list']:
        participants = event['participants']
        for participant in participants:
            if participant['role'] == 'tutor' and participant['id'] not in tutors:
                tutors.append(participant['id'])

    for tutor in tutors:
        tutor = {
            'id': tutor,
            'quality': []
        }
        for event in events['list']:
            if len(event['quality']) > 0:
                participants = event['participants']
                for participant in participants:
                    if participant['role'] == 'tutor' and participant['id'] == tutor['id']:
                        tutor['quality'].append(event['quality'][0])
        if len(tutor['quality']) > 0:
            tutor['quality'] = sum(tutor['quality']) / len(tutor['quality'])
            tutor['quality'] = round(tutor['quality'], 2)
        else:
            tutor['quality'] = None

        tutors_with_quality.append(tutor)

    tutors_with_quality = [x for x in tutors_with_quality if x['quality'] != None]
    tutors_with_quality = sorted(tutors_with_quality, key=lambda k: k['quality'])

    bad_tutor = [date, tutors_with_quality[0]['id'], tutors_with_quality[0]['quality']]
    print(bad_tutor)
