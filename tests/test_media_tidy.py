"""Tests for the pure (non-GUI) functions in media_tidy.py."""

import os
from datetime import datetime

from PIL import Image

import media_tidy


def _plain_png(path):
    """A PNG with no EXIF metadata."""
    Image.new("RGB", (10, 10), "red").save(path)


def _jpeg_with_exif(path, date_str):
    img = Image.new("RGB", (10, 10), "blue")
    exif = img.getexif()
    exif[36867] = date_str  # DateTimeOriginal
    img.save(path, exif=exif)


# --- get_file_date / get_date_taken ---

def test_get_file_date_falls_back_to_mtime_when_no_exif(tmp_path):
    target = tmp_path / "plain.png"
    _plain_png(target)
    mtime = 1_700_000_000
    os.utime(target, (mtime, mtime))

    assert media_tidy.get_file_date(str(target)) == datetime.fromtimestamp(mtime)


def test_get_file_date_prefers_exif_over_mtime(tmp_path):
    target = tmp_path / "photo.jpg"
    _jpeg_with_exif(target, "2023:01:02 03:04:05")
    os.utime(target, (1_700_000_000, 1_700_000_000))  # newer than EXIF date

    assert media_tidy.get_file_date(str(target)) == datetime(2023, 1, 2, 3, 4, 5)


def test_get_date_taken_returns_none_without_exif(tmp_path):
    target = tmp_path / "plain.png"
    _plain_png(target)
    assert media_tidy.get_date_taken(str(target)) is None


def test_get_file_date_video_uses_mtime(tmp_path):
    target = tmp_path / "clip.mp4"
    target.write_bytes(b"fake video bytes")
    mtime = 1_700_000_123
    os.utime(target, (mtime, mtime))

    assert media_tidy.get_file_date(str(target)) == datetime.fromtimestamp(mtime)


# --- process_media_file ---

def test_process_media_file_renames_and_moves(tmp_path):
    src = tmp_path / "src"
    src.mkdir()
    dest = tmp_path / "Images"
    dest.mkdir()
    photo = src / "IMG_1234.jpg"
    photo.write_bytes(b"bytes")

    media_tidy.process_media_file(str(photo), str(dest), datetime(2024, 5, 6, 7, 8, 9))

    assert not photo.exists()
    assert (dest / "2024-05-06_07-08-09.jpg").exists()


def test_process_media_file_collision_appends_counter(tmp_path):
    src = tmp_path / "src"
    src.mkdir()
    dest = tmp_path / "Images"
    dest.mkdir()
    (dest / "2024-05-06_07-08-09.jpg").write_bytes(b"already here")
    photo = src / "another.jpg"
    photo.write_bytes(b"bytes")

    media_tidy.process_media_file(str(photo), str(dest), datetime(2024, 5, 6, 7, 8, 9))

    assert (dest / "2024-05-06_07-08-09 (1).jpg").exists()


# --- cleanup_empty_folders ---

def test_cleanup_empty_folders_removes_empties_spares_protected(tmp_path):
    library = tmp_path / "library"
    empty_nested = library / "old" / "nested"
    empty_nested.mkdir(parents=True)
    images = library / "Images"
    images.mkdir()  # protected: must survive even though empty
    nonempty = library / "keep"
    nonempty.mkdir()
    (nonempty / "photo.jpg").write_bytes(b"x")

    protected = {os.path.normcase(str(images))}
    media_tidy.cleanup_empty_folders(str(library), protected)

    # The walk is bottom-up on a snapshot: a parent whose child was just
    # deleted still lists it in dirnames, so it survives a single run.
    assert not (library / "old" / "nested").exists()
    assert (library / "old").exists()
    assert images.exists()
    assert nonempty.exists()
