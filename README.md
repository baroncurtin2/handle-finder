The purpose of this challenge is mainly to get a sense of how you design and implement code while solving a problem that
involves external entities. So rather than a quick solution, we are hoping you would take a bit of time and think
through the issues involved. That said we think a reasonable solution can be implemented within 3 hours.

## Objective

Given a url, find/extract all instances of the following if present:

```angular2html
Twitter handle
Facebook page id
iOS App Store id
Google Play Store id
```

Examples:

```angular2html
url = https://www.appannie.com/
Your result should be a JSON string of the following structure:
{
"twitter": "appannie",
"facebook": "AppAnnie"
}

url = http://www.zello.com/
{
"ios": "508231856",
"google": "com.loudtalks",
"twitter": "Zello"
}

url = http://zynga.com
has multiple twitter handles on the page, but for Twitter and Facebook these are the handles for the company:
{
"twitter": "zynga",
"facebook":  "zynga"
}

```

Please design your code to be scalable, i.e., work for one url or a million urls. Please also make sure your code can
handle redirects, timeouts and badly formed urls. You also get bonus points for being PEP8 and jsonlint compliant.
Please do not use Scrapy.
