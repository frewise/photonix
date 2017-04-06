from datetime import datetime
from decimal import Decimal
import mimetypes
import os

from django.utils.timezone import UTC

from photos.models import Camera, Lens, Photo, PhotoFile
from photos.utils.metadata import PhotoMetadata, parse_datetime, get_datetime, parse_gps_location


def record_photo(path):
    file_modified_at = datetime.fromtimestamp(os.stat(path).st_mtime, tz=UTC())

    try:
        photo_file = PhotoFile.objects.get(path=path)
    except PhotoFile.DoesNotExist:
        photo_file = PhotoFile()

    if photo_file and photo_file.file_modified_at == file_modified_at:
        return False

    metadata = PhotoMetadata(path)

    camera_make = metadata.get('Make')
    camera_model = metadata.get('Camera Model Name')
    if camera_model:
        camera_model = camera_model.replace(camera_make, '').strip()
    date_taken = parse_datetime(metadata.get('Date/Time Original'))

    try:
        camera = Camera.objects.get(make=camera_make, model=camera_model)
        if date_taken < camera.earliest_photo:
            camera.earliest_photo = date_taken
            camera.save()
        if date_taken > camera.latest_photo:
            camera.latest_photo = date_taken
            camera.save()
    except Camera.DoesNotExist:
        camera = Camera(make=camera_make, model=camera_model, earliest_photo=date_taken, latest_photo=date_taken)
        camera.save()

    lens_name = metadata.get('Lens ID')

    try:
        lens = Lens.objects.get(name=lens_name)
        if date_taken < lens.earliest_photo:
            lens.earliest_photo = date_taken
            lens.save()
        if date_taken > lens.latest_photo:
            lens.latest_photo = date_taken
            lens.save()
    except Lens.DoesNotExist:
        lens = Lens(name=lens_name, earliest_photo=date_taken, latest_photo=date_taken)
        lens.save()

    try:
        # TODO: Match on file number/file name as well
        photo = Photo.objects.get(taken_at=get_datetime(path))
    except Photo.DoesNotExist:
        photo = Photo(
            taken_at=get_datetime(path),
            taken_by=metadata.get('Artist') or '',
            aperture=Decimal(metadata.get('Aperture')),
            exposure=metadata.get('Exposure Time'),
            iso_speed=int(metadata.get('ISO')),
            focal_length=metadata.get('Focal Length').split(' ', 1)[0],
            flash='on' in metadata.get('Flash').lower() or False,
            metering_mode=metadata.get('Metering Mode'),
            drive_mode=metadata.get('Drive Mode'),
            shooting_mode=metadata.get('Shooting Mode'),
            camera=camera,
            lens=lens,
            location=metadata.get('GPS Position') and parse_gps_location(metadata.get('GPS Position')) or None,
            altitude=metadata.get('GPS Altitude') and metadata.get('GPS Altitude').split(' ')[0]
        )
        photo.save()

    photo_file.photo            = photo
    photo_file.path             = path
    photo_file.width            = metadata.get('Image Width')
    photo_file.height           = metadata.get('Image Height')
    photo_file.mimetype         = mimetypes.guess_type(path)[0]
    photo_file.file_modified_at = file_modified_at
    photo_file.bytes            = os.stat(path).st_size
    photo_file.preferred        = False  # TODO
    photo_file.save()

    return True