# Generated by Django 4.1.8 on 2024-04-14 14:01

from django.db import migrations, models
import wagtail.blocks
import wagtail.fields


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0030_rename_location_blogdetailpage_address_backup_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='blogdetailpage',
            name='links',
        ),
        migrations.AddField(
            model_name='blogdetailpage',
            name='location',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='blogdetailpage',
            name='similar_page',
            field=wagtail.fields.StreamField([('link', wagtail.blocks.StructBlock([('title', wagtail.blocks.CharBlock(required=True))]))], blank=True, null=True, use_json_field=None),
        ),
        migrations.AlterField(
            model_name='blogdetailpage',
            name='date',
            field=models.PositiveIntegerField(blank=True, choices=[(1970, 1970), (1971, 1971), (1972, 1972), (1973, 1973), (1974, 1974), (1975, 1975), (1976, 1976), (1977, 1977), (1978, 1978), (1979, 1979), (1980, 1980), (1981, 1981), (1982, 1982), (1983, 1983), (1984, 1984), (1985, 1985), (1986, 1986), (1987, 1987), (1988, 1988), (1989, 1989), (1990, 1990), (1991, 1991), (1992, 1992), (1993, 1993), (1994, 1994), (1995, 1995), (1996, 1996), (1997, 1997), (1998, 1998), (1999, 1999), (2000, 2000), (2001, 2001), (2002, 2002), (2003, 2003), (2004, 2004), (2005, 2005), (2006, 2006), (2007, 2007), (2008, 2008), (2009, 2009), (2010, 2010), (2011, 2011), (2012, 2012), (2013, 2013), (2014, 2014), (2015, 2015), (2016, 2016), (2017, 2017), (2018, 2018), (2019, 2019), (2020, 2020), (2021, 2021), (2022, 2022), (2023, 2023), (2024, 2024)], default=1970, null=True, verbose_name='Post date'),
        ),
    ]
