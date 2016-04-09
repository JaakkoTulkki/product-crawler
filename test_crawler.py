# -*- coding: utf-8 -*-
from unittest import TestCase
from crawler import calculate_total_unit_costs, get_start_page_links, scrape_product_page


class TestCrawler(TestCase):

    def test_calculate_total_unit_costs(self):
        data = [{'unit_price': 1.9}, {'unit_price': 1.1}, {'unit_price': 2}, {'ko': 100}]
        total = calculate_total_unit_costs(data)
        self.assertEqual(total, 5.0, "{} is not 4.0".format(total))
        self.assertTrue(type(total) is float, "Total not float")

    def test_get_start_page_links(self):
        # html for the test
        start_page_html = """<!DOCTYPE html>
<html>
<head lang="en">
    <meta charset="UTF-8">
    <title>Test</title>
</head>
<body>

<div class="productInfoWrapper">
<div class="productInfo">
<h3>
    <a href="http://test.com" >
        Product one x5
        <img src="" alt="" />
    </a>
</h3>
<div class="ThumbnailRoundel">
<!--ThumbnailRoundel -->
</div>
<div class="promoBages">
<!-- PROMOTION -->
</div>
<!-- Review --><!-- BEGIN CatalogEntryRatingsReviewsInfo.jspf --><!-- productAllowedRatingsAndReviews: false --><!-- END CatalogEntryRatingsReviewsInfo.jspf -->
</div>
</div>
<div class="productInfoWrapper">
<div class="productInfo">
<h3>
    <a href="http://test2.com" >
        Product two Ready x5
        <img src="" alt="" />
    </a>
</h3>
<div class="ThumbnailRoundel">
<!--ThumbnailRoundel -->
</div>
<div class="promoBages">
<!-- PROMOTION -->
</div>
<!-- Review --><!-- BEGIN CatalogEntryRatingsReviewsInfo.jspf --><!-- productAllowedRatingsAndReviews: false --><!-- END CatalogEntryRatingsReviewsInfo.jspf -->
</div>
</div>
</body>
</html>"""
        links = get_start_page_links(start_page_html)
        self.assertTrue(links[0] == "http://test.com")
        self.assertTrue(links[1] == "http://test2.com")


    def test_scrape_product_page(self):
        # test html to scrape
        test_html = """<!DOCTYPE html>
<html>
<head lang="en">
    <meta charset="UTF-8">
    <meta name="description" content="Buy this product"/>
    <title></title>
</head>
<body>
<div class="productSummary">
<div class="productTitleDescriptionContainer">
<h1>Sainsbury's Apricot Ripe & Ready x5</h1>

<div id="productImageHolder">
     <img src="http://www.sainsburys.co.uk/wcsstore7.11.1.161/SainsburysStorefrontAssetStore/wcassets/product_images/media_7572754_L.jpg"  alt="Image for Sainsbury&#039;s Apricot Ripe &amp; Ready x5 from Sainsbury&#039;s" class="productImage " id="productImageID" />
</div>
<div class="reviews">
    <!-- BEGIN CatalogEntryRatingsReviewsInfoDetailsPage.jspf --><!-- END CatalogEntryRatingsReviewsInfoDetailsPage.jspf -->
</div>
</div>

<div class="addToTrolleytabBox" >
<!-- Start UserSubscribedOrNot.jspf --><!-- Start UserSubscribedOrNot.jsp --><!--
If the user is not logged in, render this opening
DIV adding an addtional class to fix the border top which is removed
and replaced by the tabs
-->
<div class="addToTrolleytabContainer addItemBorderTop">
<!-- End AddToSubscriptionList.jsp --><!-- End AddSubscriptionList.jspf --><!--
ATTENTION!!!
<div class="addToTrolleytabContainer">
This opening div is inside "../../ReusableObjects/UserSubscribedOrNot.jsp"
-->
<div class="pricingAndTrolleyOptions">

<div class="priceTab activeContainer priceTabContainer" id="addItem_149117"> <!-- CachedProductOnlyDisplay.jsp -->
    <div class="pricing">

    <p class="pricePerUnit">
    &pound;3.50<abbr title="per">/</abbr><abbr title="unit"><span class="pricePerUnitUnit">unit</span></abbr>
    </p>
    </div>
</div>
</div>
</div>
</div>
</div>
</body>
</html>"""
        data = scrape_product_page(test_html)
        correct_data = {'description': 'Buy this product',
                        'size': '1.63 KB', # do not modify the the test_html or otherwise this will fail
                         'title': "Sainsbury's Apricot Ripe & Ready x5",
                         'unit_price': 3.5
                        }
        self.assertEqual(data, correct_data, "Incorrect data {} is not {}".format(data, correct_data))
