from django.db import models

    # TODO: remember that JSON output will inflate this data model
    # - adding @type (left implicit here)
    # - amenityFeature needs several more attributes autopopulated

class MapReference(models.Model):
    route_point = models.ForeignKey('RoutePoint', on_delete=models.CASCADE)
    map_series = models.CharField(max_length=10)
    map_number = models.CharField(max_length=10)
    grid_reference = models.CharField(max_length=10)

class PersonAndOrganization(models.Model):
    name = models.CharField(max_length=100, verbose_name='Name')
    email = models.EmailField(verbose_name='Email', blank=True)
    website = models.URLField(verbose_name='Website', blank=True)
    map_reference = models.ForeignKey(MapReference, on_delete=models.CASCADE, verbose_name='publisher', blank=True, null=True)

class Provenance(models.Model):
    publisher = models.ForeignKey(PersonAndOrganization, on_delete=models.CASCADE)
    url = models.URLField()
    version = models.DateField(auto_now=False, auto_now_add=False)
    description = models.CharField(max_length=250)

class Category(models.Model):
    content = models.CharField(max_length=30)

class Article(models.Model):
    headline = models.CharField(max_length=100)
    body = models.TextField()
    backstory = models.TextField()

class GeoPath(models.Model):
    route_guide = models.ForeignKey('RouteGuide', on_delete=models.CASCADE, blank=True, null=True)
    route_guide_segment = models.ForeignKey('RouteGuideSegment', on_delete=models.CASCADE, blank=True, null=True)
    map_type = models.CharField(max_length=12, choices=[("RouteMap", "RouteMap"), ("ElevationMap", "ElevationMap"), ("CustomMap", "CustomMap")])
    url = models.URLField()
    encoding_format = models.CharField(max_length=40)

class MapImage(models.Model):
    route_guide = models.ForeignKey('RouteGuide', on_delete=models.CASCADE, blank=True, null=True)
    route_guide_segment = models.ForeignKey('RouteGuideSegment', on_delete=models.CASCADE, blank=True, null=True)
    map_type = models.CharField(max_length=12, choices=[("RouteMap", "RouteMap"), ("ElevationMap", "ElevationMap"), ("CustomMap", "CustomMap")])
    image = models.URLField()
    encoding_format = models.CharField(max_length=40)

class VerificationRecord(models.Model):
    verified_by = models.ManyToManyField(PersonAndOrganization, verbose_name='Verified By')
    date_verified = models.DateField(auto_now=False, auto_now_add=False, verbose_name='Date Verified')

class Distance(models.Model):
    route_point = models.ForeignKey('RoutePoint', on_delete=models.CASCADE, blank=True, null=True, related_name="elevation")
    value = models.FloatField(verbose_name='Distance')
    unit = models.CharField(max_length=6, verbose_name='Unit', default="km")

class AccessibilityDescription(models.Model):
    route_guide = models.ForeignKey('RouteGuide', on_delete=models.CASCADE, blank=True, null=True)
    route_guide_segment = models.ForeignKey('RouteGuideSegment', on_delete=models.CASCADE, blank=True, null=True)
    description = models.CharField(max_length=250, verbose_name='')

class Activity(models.Model):
    prefLabel = models.CharField(max_length=100, verbose_name='Preferred Label (English)')
    identifier = models.URLField(verbose_name='Identifier')

class IndicativeDuration(models.Model):
    duration = models.CharField(max_length=10, verbose_name='Duration (8601)') # TODO: Add regex for validation

class RoutePoint(models.Model):
    route_guide = models.ForeignKey('RouteGuide', on_delete=models.CASCADE, blank=True, null=True)
    route_guide_segment = models.ForeignKey('RouteGuideSegment', on_delete=models.CASCADE, blank=True, null=True)
    name = models.CharField(max_length=100, verbose_name='Name')
    is_access_point = models.BooleanField(verbose_name='Is Access Point')
    is_preferred_access_point = models.BooleanField(verbose_name='Is Preferred Access Point')
    description = models.TextField(blank=True, verbose_name='Description')
    headline = models.CharField(blank=True, max_length=200, verbose_name='Headline (Brief Description)')
    same_as = models.URLField(verbose_name='Same As')

class AmenityFeature(models.Model):
    route_point = models.ForeignKey(RoutePoint, on_delete=models.CASCADE)
    name = models.CharField(max_length=75)

class GeoCoordinates(models.Model):
    route_point = models.ForeignKey(RoutePoint, on_delete=models.CASCADE, blank=True, null=True)
    latitude = models.FloatField(verbose_name='Latitude')
    longitude = models.FloatField(verbose_name='Longitude')

class RouteGradient(models.Model):
    route_guide = models.ForeignKey('RouteGuide', on_delete=models.CASCADE, blank=True, null=True)
    route_guide_segment = models.ForeignKey('RouteGuideSegment', on_delete=models.CASCADE, blank=True, null=True)
    max_gradient = models.CharField(max_length=10, default='0%')
    avg_gradient = models.CharField(max_length=10, default='0%')
    total_elevation_gain = models.ForeignKey(Distance, on_delete=models.CASCADE, related_name='total_elevation_gain')
    total_elevation_loss = models.ForeignKey(Distance, on_delete=models.CASCADE, related_name='total_elevation_loss')
    gradient_term = models.CharField(max_length=100, verbose_name='Gradient Term')
    gradient_defurl = models.URLField(verbose_name='Gradient Definition URL')
    description = models.CharField(max_length=250)

class RouteDifficulty(models.Model):
    difficulty_term = models.CharField(max_length=15)
    description = models.CharField(max_length=250)
    difficulty_defurl = models.URLField(verbose_name='Difficulty Definition URL')

class TransportNote(models.Model):
    route_point = models.ForeignKey(RoutePoint, on_delete=models.CASCADE, blank=True, null=True)
    transport_mode = models.CharField(max_length=100, choices=[("Bus", "Bus"), ("Rail", "Rail"), ("Road", "Road"), ("Foot", "Foot"), ("Bicycle", "Bicycle")])
    description = models.CharField(max_length=500)

class RouteLegalAdvisory(models.Model):
    route_guide = models.ForeignKey('RouteGuide', on_delete=models.CASCADE, blank=True, null=True)
    route_guide_segment = models.ForeignKey('RouteGuideSegment', on_delete=models.CASCADE, blank=True, null=True)
    route_designation = models.ForeignKey('RouteDesignation', on_delete=models.CASCADE, verbose_name='Route Designation')
    description = models.CharField(max_length=250)
    legal_defurl = models.URLField(verbose_name='Legal Definition URL')

class RouteDesignation(models.Model):
    # TODO: give dropdown suggestions for route designations in front end
    route_des_term = models.CharField(max_length=100, verbose_name='Route Designation Term')
    description = models.CharField(max_length=250)
    url = models.URLField(verbose_name='Formal Definition URL')

class RouteSegmentGroup(models.Model):
    id_as_url = models.URLField(verbose_name='@id', blank=False)
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=250)
    segments = models.ManyToManyField('RouteGuideSegment', verbose_name='Includes Segments')
    alternatives = models.ForeignKey('RouteSegmentGroup', on_delete=models.CASCADE, verbose_name='Alternative Group To')

class UserGeneratedContent(models.Model):
    creator = models.ForeignKey(PersonAndOrganization, on_delete=models.CASCADE, related_name='created_by')
    accountable_person = models.ForeignKey(PersonAndOrganization, on_delete=models.CASCADE)
    spatial_coverage = models.CharField(max_length=500)
    associated_media = models.CharField(max_length=500)

class RouteGuide(models.Model):
    # TODO: check blank values permitted align with specification
    name = models.CharField(max_length=200, verbose_name='Name')
    url = models.URLField(verbose_name='Trackback URL')
    date_published = models.DateField(blank=True,auto_now=False, auto_now_add=False, verbose_name='Date Published')
    date_modified = models.DateField(blank=True, auto_now=False, auto_now_add=False, verbose_name='Date Modified')
    description = models.TextField(blank=True, verbose_name='Description')
    headline = models.CharField(blank=True, max_length=200, verbose_name='Headline (Brief Description)')
    is_loop = models.BooleanField(verbose_name='Is Loop', default=True)
    id_as_url = models.URLField(primary_key=True, verbose_name='ID (URL)')
    is_based_on = models.ForeignKey(Provenance, on_delete=models.CASCADE, blank=True, null=True)
    author = models.ManyToManyField(PersonAndOrganization, verbose_name='Author')
    verification_record = models.ForeignKey(VerificationRecord, on_delete=models.CASCADE, blank=True, null=True)
    activity = models.ManyToManyField(Activity)
    route_difficulty = models.ForeignKey(RouteDifficulty, on_delete=models.CASCADE, blank=True, null=True)
    distance = models.ForeignKey(Distance, on_delete=models.CASCADE, null=True)

class RouteGuideSegment(models.Model):
    # TODO: check blank values permitted align with specification
    name = models.CharField(max_length=200, verbose_name='Name')
    url = models.URLField(verbose_name='Trackback URL')
    date_published = models.DateField(blank=True,auto_now=False, auto_now_add=False, verbose_name='Date Published')
    date_modified = models.DateField(blank=True, auto_now=False, auto_now_add=False, verbose_name='Date Modified')
    description = models.TextField(blank=True, verbose_name='Description')
    headline = models.CharField(blank=True, max_length=200, verbose_name='Headline (Brief Description)')
    is_loop = models.BooleanField(verbose_name='Is Loop', default=True)
    id_as_url = models.URLField(primary_key=True, verbose_name='ID (URL)')
    segment = models.IntegerField(verbose_name='Segment Number')
    top_level_route_guide = models.ForeignKey(RouteGuide, on_delete=models.CASCADE, blank=False)
    verification_record = models.ForeignKey(VerificationRecord, on_delete=models.CASCADE, blank=True, null=True)
    activity = models.ManyToManyField(Activity)
    route_difficulty = models.ForeignKey(RouteDifficulty, on_delete=models.CASCADE, blank=True, null=True)
    distance = models.ForeignKey(Distance, on_delete=models.CASCADE, null=True)
    category = models.ManyToManyField(Category)
    additional_info = models.ManyToManyField(Article)
