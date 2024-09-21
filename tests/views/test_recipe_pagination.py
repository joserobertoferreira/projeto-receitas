from unittest import TestCase

from resources.utils.pagination import set_pagination_range


class PaginationTest(TestCase):
    def test_create_set_pagination_range(self):
        pagination = set_pagination_range(
            page_range=list(range(1, 21)),
            view_pages=4,
            current_page=1,
        )['pagination']

        self.assertEqual([1, 2, 3, 4], pagination)  # noqa: PT009

    def test_first_range_no_change_if_less_than_middle_page(self):
        pagination = set_pagination_range(
            page_range=list(range(1, 21)),
            view_pages=4,
            current_page=1,
        )['pagination']

        self.assertEqual([1, 2, 3, 4], pagination)  # noqa: PT009

        pagination = set_pagination_range(
            page_range=list(range(1, 21)),
            view_pages=4,
            current_page=2,
        )['pagination']

        self.assertEqual([1, 2, 3, 4], pagination)  # noqa: PT009

        pagination = set_pagination_range(
            page_range=list(range(1, 21)),
            view_pages=4,
            current_page=3,
        )['pagination']

        self.assertEqual([2, 3, 4, 5], pagination)  # noqa: PT009

        pagination = set_pagination_range(
            page_range=list(range(1, 21)),
            view_pages=4,
            current_page=4,
        )['pagination']

        self.assertEqual([3, 4, 5, 6], pagination)  # noqa: PT009

    def test_range_for_middle_page(self):
        pagination = set_pagination_range(
            page_range=list(range(1, 21)),
            view_pages=4,
            current_page=10,
        )['pagination']

        self.assertEqual([9, 10, 11, 12], pagination)  # noqa: PT009

        pagination = set_pagination_range(
            page_range=list(range(1, 21)),
            view_pages=4,
            current_page=14,
        )['pagination']

        self.assertEqual([13, 14, 15, 16], pagination)  # noqa: PT009

    def test_last_range_no_change_if_more_than_middle_page(self):
        pagination = set_pagination_range(
            page_range=list(range(1, 21)),
            view_pages=4,
            current_page=18,
        )['pagination']

        self.assertEqual([17, 18, 19, 20], pagination)  # noqa: PT009

        pagination = set_pagination_range(
            page_range=list(range(1, 21)),
            view_pages=4,
            current_page=19,
        )['pagination']

        self.assertEqual([17, 18, 19, 20], pagination)  # noqa: PT009

        pagination = set_pagination_range(
            page_range=list(range(1, 21)),
            view_pages=4,
            current_page=20,
        )['pagination']

        self.assertEqual([17, 18, 19, 20], pagination)  # noqa: PT009

        pagination = set_pagination_range(
            page_range=list(range(1, 21)),
            view_pages=4,
            current_page=21,
        )['pagination']

        self.assertEqual([17, 18, 19, 20], pagination)  # noqa: PT009
