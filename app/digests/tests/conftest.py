from typing import Dict, List

from django.conf import settings
import pytest
from rest_framework.test import APIClient

from digests.models import Digest


@pytest.fixture
@pytest.mark.django_db
def rest_client() -> APIClient:
    return APIClient()


@pytest.fixture
def can_preview_header():
    return {settings.CONSUMER_GROUPS_HEADER: 'view-unpublished-content'}


@pytest.fixture
def can_edit_headers():
    return {settings.CONSUMER_GROUPS_HEADER: 'view-unpublished-content, edit-digests'}


@pytest.fixture
def preview_digest(digest_json: Dict) -> Digest:
    return Digest.objects.create(id=digest_json['id'],
                                 content=digest_json['content'],
                                 image=digest_json['image'],
                                 impactStatement=digest_json['impactStatement'],
                                 published=digest_json['published'],
                                 relatedContent=digest_json['relatedContent'],
                                 subjects=digest_json['subjects'],
                                 title=digest_json['title'])


@pytest.fixture
def published_digest(digest_json: Dict) -> Digest:
    return Digest.objects.create(id='3',
                                 content=digest_json['content'],
                                 image=digest_json['image'],
                                 impactStatement=digest_json['impactStatement'],
                                 published=digest_json['published'],
                                 relatedContent=digest_json['relatedContent'],
                                 stage='published',
                                 subjects=digest_json['subjects'],
                                 title=digest_json['title'])


@pytest.fixture(scope='session')
def digest_content_json() -> List[Dict]:
    return [
        {
            "type": "paragraph",
            "text": "Small roundworms such as <i>Caenorhabditis elegans</i> "
                    "release chemical signals called ascarosides in order to "
                    "communicate with other worms of the same species. Using the "
                    "ascarosides, the worm can tell its friends, for example, "
                    "how crowded the neighborhood is and whether there is enough "
                    "food. The ascarosides thus help the worms in the population "
                    "decide whether the neighborhood is good — meaning they "
                    "should hang around, eat, and make babies — or whether the "
                    "neighborhood is bad. If so, the worms should develop into a "
                    "larval stage specialized for dispersal that will allow them "
                    "to find a better neighborhood."
        },
        {
            "type": "image",
            "image": {
                "uri": "https://iiif.elifesciences.org/medium:1*UaX-QIG8sgCXp6BDzc617w.jpeg",
                "alt": "",
                "attribution": [
                    "<a href=\"https://commons.wikimedia.org/wiki/File:Neighbourhood_Watch_;-%29.JPG\">"
                    "UliDolbarge</a> (<a href=\"https://creativecommons.org/licenses/by-sa/4.0/deed.en\">"
                    "CC BY-SA 4.0</a>)"
                ],
                "source": {
                    "mediaType": "image/jpeg",
                    "uri": "https://cdn-images-1.medium.com/1*UaX-QIG8sgCXp6BDzc617w.jpeg",
                    "filename": "1 UaX-QIG8sgCXp6BDzc617w.jpeg"
                },
                "size": {
                    "width": 1152,
                    "height": 864
                },
                "focalPoint": {
                    "x": 25,
                    "y": 75
                }
            },
            "title": "“God sees everything – the neighbors see more”"
        },
        {
            "type": "paragraph",
            "text": "Roundworms make the ascarosides by attaching a long "
                    "chemical ‘side chain’ to an ascarylose sugar. Further "
                    "chemical modifications allow the worms to produce different "
                    "signals. In general, to signal a good neighborhood, worms "
                    "attach a structure called an indole group to the "
                    "ascarosides. To signal a bad neighborhood, worms make the "
                    "side chain very short. But how does a worm control which "
                    "ascarosides it makes?"
        },
        {
            "type": "paragraph",
            "text": "Zhou, Wang et al. now show that <i>C. elegans</i> can "
                    "change the meaning of its chemical message by modifying the "
                    "ascarosides that it has already produced instead of making "
                    "new ones from scratch. Specifically, as their neighborhood "
                    "runs out of food, <i>C. elegans</i> can use an enzyme "
                    "called ACS-7 to initiate the shortening of the side chains "
                    "of indole-ascarosides. The worm can thus change a favorable "
                    "ascaroside signal that causes the worms to group together "
                    "into an unfavorable ascaroside signal that causes the worms "
                    "to enter their dispersal stage."
        },
        {
            "type": "paragraph",
            "text": "Although Zhou, Wang et al. have focused on chemical "
                    "communication in <i>C. elegans</i>, the findings could "
                    "easily apply to the many other species of roundworm that "
                    "produce ascarosides. Knowing how worms communicate will "
                    "help us to understand how worms respond to their "
                    "environment. This knowledge could potentially be used to "
                    "interfere with the lifecycles and survival of parasitic "
                    "worm species that harm health and crops."
        }
    ]


@pytest.fixture(scope='session')
def digest_image_json() -> Dict:
    return {
        "thumbnail": {
            "uri": "https://iiif.elifesciences.org/medium:1*UaX-QIG8sgCXp6BDzc617w.jpeg",
            "alt": "",
            "source": {
                "mediaType": "image/jpeg",
                "uri": "https://cdn-images-1.medium.com/1*UaX-QIG8sgCXp6BDzc617w.jpeg",
                "filename": "1 UaX-QIG8sgCXp6BDzc617w.jpeg"
            },
            "size": {
                "width": 1152,
                "height": 864
            },
            "focalPoint": {
                "x": 25,
                "y": 75
            }
        }
    }


@pytest.fixture(scope='session')
def digest_related_content_json() -> List[Dict]:
    return [
        {
            "type": "research-article",
            "status": "vor",
            "id": "33286",
            "version": 1,
            "doi": "10.7554/eLife.33286",
            "authorLine": "Yue Zhou et al.",
            "title": "Biosynthetic tailoring of existing ascaroside pheromones "
                     "alters their biological function in <i>C. elegans</i>",
            "stage": "published",
            "published": "2018-06-04T00:00:00Z",
            "statusDate": "2018-06-04T00:00:00Z",
            "volume": 7,
            "elocationId": "e33286"
        }
    ]


@pytest.fixture(scope='session')
def digest_subjects_json() -> List[Dict]:
    return [
        {
            "id": "biochemistry-chemical-biology",
            "name": "Biochemistry and Chemical Biology"
        }
    ]


@pytest.fixture(scope='session')
def digest_json(digest_image_json: Dict,
                digest_content_json: List[Dict],
                digest_related_content_json: List[Dict],
                digest_subjects_json: List[Dict]) -> Dict:
    return {
        "id": "2",
        "title": "Neighborhood watch",
        "impactStatement": "Roundworms modify the chemical signals they produce to"
                           " tell others whether they’re in a good or bad environment.",
        "stage": "preview",
        "published": "2018-07-06T09:06:01Z",
        "image": digest_image_json,
        "subjects": digest_subjects_json,
        "content": digest_content_json,
        "relatedContent": digest_related_content_json
    }
