from door_light.dioda import Dioda
from project_settings.settings import load_settings


def run_door_light(settings):
    door_light_settings = settings['DL']
    door_light = Dioda(door_light_settings['pin'], door_light_settings['simulated'])
    door_light.run([])


if __name__ == '__main__':
    settings = load_settings()
    run_door_light(settings)
