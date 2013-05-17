from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from django.utils.timezone import now
from django.conf import settings
from uphotos.managers import PhotoManager
from follow import utils

# Create your models here.

# Quality options for JPEG images
JPEG_QUALITY_CHOICES = (
    (30, _('Very Low')),
    (40, _('Low')),
    (50, _('Medium-Low')),
    (60, _('Medium')),
    (70, _('Medium-High')),
    (80, _('High')),
    (90, _('Very High')),
)

# choices for new crop_anchor field in Photo
CROP_ANCHOR_CHOICES = (
    ('top', _('Top')),
    ('right', _('Right')),
    ('bottom', _('Bottom')),
    ('left', _('Left')),
    ('center', _('Center (Default)')),
)

IMAGE_TRANSPOSE_CHOICES = (
    ('FLIP_LEFT_RIGHT', _('Flip left to right')),
    ('FLIP_TOP_BOTTOM', _('Flip top to bottom')),
    ('ROTATE_90', _('Rotate 90 degrees counter-clockwise')),
    ('ROTATE_270', _('Rotate 90 degrees clockwise')),
    ('ROTATE_180', _('Rotate 180 degrees')),
)

# Default limit for gallery.latest
LATEST_LIMIT = getattr(settings, 'PHOTOLOGUE_GALLERY_LATEST_LIMIT', None)

# attempt to load the django-tagging TagField from default location,
# otherwise we substitude a dummy TagField.
try:
    from tagging.fields import TagField
    tagfield_help_text = _('Separate tags with spaces, put quotes around multiple-word tags.')
except ImportError:
    class TagField(models.CharField):
        def __init__(self, **kwargs):
            default_kwargs = {'max_length': 255, 'blank': True}
            default_kwargs.update(kwargs)
            super(TagField, self).__init__(**default_kwargs)
        def get_internal_type(self):
            return 'CharField'
    tagfield_help_text = _('Django-tagging was not found, tags will be treated as plain text.')

    # Tell South how to handle this custom field.
    from south.modelsinspector import add_introspection_rules
    add_introspection_rules([], ["^uphotos\.models\.TagField"])

class ImageModel(models.Model):
    #image = models.ImageField(_('image'), max_length=IMAGE_FIELD_MAX_LENGTH,
                              #upload_to=get_storage_path)
    image_url = models.URLField(null=True)
    date_taken = models.DateTimeField(_('date taken'), null=True, blank=True, editable=False)
    view_count = models.PositiveIntegerField(default=0, editable=False)
    crop_from = models.CharField(_('crop from'), blank=True, max_length=10, default='center', choices=CROP_ANCHOR_CHOICES)

    class Meta:
        abstract = True


class Photo(ImageModel):
    caption = models.TextField(_('caption'), blank=True)
    date_added = models.DateTimeField(_('date added'), default=now)
    is_public = models.BooleanField(_('is public'), default=True, help_text=_('Public photographs will be displayed in the default views.'))
    tags = TagField(help_text=tagfield_help_text, verbose_name=_('tags'))
    
    publisher = models.ForeignKey(User)
    is_avatar = models.BooleanField(_('is avatar'), default=False, help_text=_('Avatar will be displayed in the Avatar views.'))
    is_confirm = models.BooleanField(_('is comfirm'),default=False, help_text=_('confirmed from upyun'))
    
    objects = PhotoManager()

    class Meta:
        ordering = ['-date_added']
        get_latest_by = 'date_added'
        verbose_name = _("photo")
        verbose_name_plural = _("photos")

    def __unicode__(self):
        return self.title

    def __str__(self):
        return self.__unicode__()

    def save(self, *args, **kwargs):
        if self.title_slug is None:
            self.title_slug = slugify(self.title)
        super(Photo, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('pl-photo', args=[self.title_slug])

    def public_galleries(self):
        """Return the public galleries to which this photo belongs."""
        return self.galleries.filter(is_public=True)

    def get_previous_in_gallery(self, gallery):
        try:
            return self.get_previous_by_date_added(galleries__exact=gallery,
                                                   is_public=True)
        except Photo.DoesNotExist:
            return None

    def get_next_in_gallery(self, gallery):
        try:
            return self.get_next_by_date_added(galleries__exact=gallery,
                                               is_public=True)
        except Photo.DoesNotExist:
            return None


class Gallery(models.Model):
    date_added = models.DateTimeField(_('date published'), default=now)
    title = models.CharField(_('title'), max_length=50, unique=True)
    title_slug = models.SlugField(_('title slug'), unique=True,
                                  help_text=_('A "slug" is a unique URL-friendly title for an object.'))
    description = models.TextField(_('description'), blank=True)
    is_public = models.BooleanField(_('is public'), default=True,
                                    help_text=_('Public galleries will be displayed in the default views.'))
    photos = models.ManyToManyField('Photo', related_name='galleries', verbose_name=_('photos'),
                                    null=True, blank=True)
    tags = TagField(help_text=tagfield_help_text, verbose_name=_('tags'))

    class Meta:
        ordering = ['-date_added']
        get_latest_by = 'date_added'
        verbose_name = _('gallery')
        verbose_name_plural = _('galleries')

    def __unicode__(self):
        return self.title

    def __str__(self):
        return self.__unicode__()

    def get_absolute_url(self):
        return reverse('pl-gallery', args=[self.title_slug])

    def latest(self, limit=LATEST_LIMIT, public=True):
        if not limit:
            limit = self.photo_count()
        if public:
            return self.public()[:limit]
        else:
            return self.photos.all()[:limit]

    def sample(self, count=None, public=True):
        """Return a sample of photos, ordered at random.
        If the 'count' is not specified, it will return a number of photos 
        limited by the GALLERY_SAMPLE_SIZE setting.
        """
        if not count:
            count = SAMPLE_SIZE
        if count > self.photo_count():
            count = self.photo_count()
        if public:
            photo_set = self.public()
        else:
            photo_set = self.photos.all()
        return random.sample(set(photo_set), count)

    def photo_count(self, public=True):
        """Return a count of all the photos in this gallery."""
        if public:
            return self.public().count()
        else:
            return self.photos.all().count()
    photo_count.short_description = _('count')

    def public(self):
        """Return a queryset of all the public photos in this gallery."""
        return self.photos.filter(is_public=True)

utils.register(Photo)
#utils.register(User)
