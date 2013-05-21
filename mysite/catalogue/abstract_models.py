from django.db import models
from django.db.models import Sum, Count, get_model
from django.utils.translation import ugettext_lazy as _

from decimal import Decimal

class AbstractProductClass(models.Model):
    """
    Used for defining options and attributes for a subset of products.
    E.g. Books, DVDs and Toys. A product can only belong to one product class.

    At least one product class must be created when setting up a new
    Oscar deployment.

    Not necessarily equivalent to top-level categories but usually will be.
    """
    name = models.CharField(_('Name'), max_length=128)
    slug = models.SlugField(_('Slug'), max_length=128, unique=True)

    #: Some product type don't require shipping (eg digital products) - we use
    #: this field to take some shortcuts in the checkout.
    requires_shipping = models.BooleanField(_("Requires shipping?"),
                                            default=True)

    #: Digital products generally don't require their stock levels to be
    #: tracked.
    track_stock = models.BooleanField(_("Track stock levels?"), default=False)

    #: These are the options (set by the user when they add to basket) for this
    #: item class.  For instance, a product class of "SMS message" would always
    #: require a message to be specified before it could be bought.
    options = models.ManyToManyField('catalogue.Option', blank=True,
                                     verbose_name=_("Options"))

    class Meta:
        abstract = True
        ordering = ['name']
        verbose_name = _("Product Class")
        verbose_name_plural = _("Product Classes")

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        return super(AbstractProductClass, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.name


class AbstractProduct(models.Model):
    """
    The base product object

    If an item has no parent, then it is the "canonical" or abstract version
    of a product which essentially represents a set of products.  If a
    product has a parent then it is a specific version of a catalogue.

    For example, a canonical product would have a title like "Green fleece"
    while its children would be "Green fleece - size L".
    """
    #: Universal product code
    upc = models.CharField(_("UPC"), max_length=64, blank=True, null=True,
                           unique=True,
        help_text=_("Universal Product Code (UPC) is an identifier for "
                    "a product which is not specific to a particular "
                    " supplier. Eg an ISBN for a book."))

    # No canonical product should have a stock record as they cannot be bought.
    parent = models.ForeignKey('self', null=True, blank=True,
                               related_name='variants',
                               verbose_name=_("Parent"),
        help_text=_("Only choose a parent product if this is a 'variant' of "
                    "a canonical catalogue.  For example if this is a size "
                    "4 of a particular t-shirt.  Leave blank if this is a "
                    "CANONICAL PRODUCT (ie there is only one version of this "
                    "product)."))

    # Title is mandatory for canonical products but optional for child products
    title = models.CharField(_('Title'), max_length=255, blank=True, null=True)
    slug = models.SlugField(_('Slug'), max_length=255, unique=False)
    description = models.TextField(_('Description'), blank=True, null=True)

    #: Use this field to indicate if the product is inactive or awaiting
    #: approval
    status = models.CharField(_('Status'), max_length=128, blank=True,
                              null=True, db_index=True)
    product_class = models.ForeignKey(
        'catalogue.ProductClass', verbose_name=_('Product Class'), null=True,
        help_text=_("""Choose what type of product this is"""))

    date_created = models.DateTimeField(_("Date Created"), auto_now_add=True)

    # This field is used by Haystack to reindex search
    date_updated = models.DateTimeField(_("Date Updated"), auto_now=True,
                                        db_index=True)
    cost_price = models.DecimalField(_("Cost Price"), decimal_places=2, max_digits=12, blank=True, null=True)
    objects = models.Manager()

    def __init__(self, *args, **kwargs):
        super(AbstractProduct, self).__init__(*args, **kwargs)
        self.attr = ProductAttributesContainer(product=self)

    # Properties

    @property
    def options(self):
        pclass = self.get_product_class()
        if pclass:
            return list(chain(self.product_options.all(),
                              self.get_product_class().options.all()))
        return self.product_options.all()

    @property
    def is_top_level(self):
        """
        Test if this product is a parent (who may or may not have children)
        """
        return self.parent_id is None

    @property
    def is_group(self):
        """
        Test if this is a top level product and has more than 0 variants
        """
        # use len() instead of count() in this specific instance
        # as variants are highly likely to be used after this
        # which reduces the amount of SQL queries required
        return self.is_top_level and len(self.variants.all()) > 0

    @property
    def is_variant(self):
        """Return True if a product is not a top level product"""
        return not self.is_top_level

    @property
    def is_shipping_required(self):
        return self.product_class.requires_shipping

    @property
    def is_available_to_buy(self):
        """
        Test whether this product is available to be purchased
        """
        if self.is_group:
            # If any one of this product's variants is available, then we treat
            # this product as available.
            for variant in self.variants.select_related('stockrecord').all():
                if variant.is_available_to_buy:
                    return True
            return False
        if not self.get_product_class().track_stock:
            return True
        return self.has_stockrecord and self.stockrecord.is_available_to_buy

    @property
    def has_stockrecord(self):
        """
        Test if this product has a stock record
        """
        try:
            self.stockrecord
        except ObjectDoesNotExist:
            return False
        else:
            return True

    def is_purchase_permitted(self, user, quantity):
        """
        Test whether this product can be bought by the passed user.
        """
        if not self.has_stockrecord:
            return False, _("No stock available")
        return self.stockrecord.is_purchase_permitted(user, quantity)


    def get_title(self):
        """
        Return a product's title or it's parent's title if it has no title
        """
        title = self.title
        if not title and self.parent_id:
            title = self.parent.title
        return title
    get_title.short_description = _("Title")

    def get_product_class(self):
        """
        Return a product's item class
        """
        if self.product_class:
            return self.product_class
        if self.parent and self.parent.product_class:
            return self.parent.product_class
        return None
    get_product_class.short_description = _("Product class")

    def get_missing_image(self):
        """
        Returns a missing image object.
        """
        # This class should have a 'name' property so it mimics the Django file
        # field.
        return MissingProductImage()

    def primary_image(self):
        images = self.images.all()
        if images.count():
            return images[0]
        # We return a dict with fields that mirror the key properties of the
        # ProductImage class so this missing image can be used interchangably
        # in templates.  Strategy pattern ftw!
        return {
            'original': self.get_missing_image(),
            'caption': '',
            'is_missing': True}

    # Helpers

    def _min_variant_price(self, property):
        """
        Return minimum variant price
        """
        prices = []
        for variant in self.variants.all():
            if variant.has_stockrecord:
                prices.append(getattr(variant.stockrecord, property))
        if not prices:
            return None
        prices.sort()
        return prices[0]

    class Meta:
        abstract = True
        ordering = ['-date_created']
        verbose_name = _('Product')
        verbose_name_plural = _('Products')

    def __unicode__(self):
        if self.is_variant:
            return u"%s (%s)" % (self.get_title(), self.attribute_summary())
        return self.get_title()

    @models.permalink
    def get_absolute_url(self):
        u"""Return a product's absolute url"""
        return ('catalogue:detail', (), {
            'product_slug': self.slug,
            'pk': self.id})

    def save(self, *args, **kwargs):
        if self.is_top_level and not self.title:
            raise ValidationError(_("Canonical products must have a title"))
        if not self.slug:
            self.slug = slugify(self.get_title())

        # Validate attributes if necessary
        self.attr.validate_attributes()

        # Save product
        super(AbstractProduct, self).save(*args, **kwargs)

        # Finally, save attributes
        self.attr.save()

class AbstractCoin(models.Model):
     """ abstract currency  model """
     exchange_rate = models.DecimalField(
         max_digits=16,
         decimal_places=8,
         default=Decimal("0.0"))

     class Meta:
        abstract = True
        verbose_name = _("Coin")
        verbose_name_plural = _("Coins")


class AbstractOption(models.Model):
    """
    An option that can be selected for a particular item when the product
    is added to the basket.

    For example,  a list ID for an SMS message send, or a personalised message
    to print on a T-shirt.

    This is not the same as an 'attribute' as options do not have a fixed value
    for a particular item.  Instead, option need to be specified by a customer
    when add the item to their basket.
    """
    name = models.CharField(_("Name"), max_length=128)
    code = models.SlugField(_("Code"), max_length=128, unique=True)

    REQUIRED, OPTIONAL = ('Required', 'Optional')
    TYPE_CHOICES = (
        (REQUIRED, _("Required - a value for this option must be specified")),
        (OPTIONAL, _("Optional - a value for this option can be omitted")),
    )
    type = models.CharField(_("Status"), max_length=128, default=REQUIRED,
                            choices=TYPE_CHOICES)

    class Meta:
        abstract = True
        verbose_name = _("Option")
        verbose_name_plural = _("Options")

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.code:
            self.code = slugify(self.name)
        super(AbstractOption, self).save(*args, **kwargs)

    @property
    def is_required(self):
        return self.type == self.REQUIRED
