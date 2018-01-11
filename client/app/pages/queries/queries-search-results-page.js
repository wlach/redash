import moment from 'moment';
import { isString } from 'underscore';

import { Paginator } from '@/lib/pagination';
import template from './queries-search-results-page.html';

function QuerySearchCtrl($location, $filter, currentUser, Events, Query) {
  this.term = $location.search().q;
  this.paginator = new Paginator([], { itemsPerPage: 20 });

  Query.search({ q: this.term, include_drafts: true }, (results) => {
    const queries = results.map((query) => {
      query.created_at = moment(query.created_at);
      return query;
    });

    this.paginator.updateRows(queries);
  });

  this.createdAtSort = row => row.created_at.valueOf();
  this.createdBySort = row => row.user.name;
  this.scheduleSort = row => row.schedule && parseInt(row.schedule, 10);

  this.search = () => {
    if (!isString(this.term) || this.term.trim() === '') {
      this.paginator.updateRows([]);
    } else {
      $location.search({ q: this.term });
    }
  };
}

export default function init(ngModule) {
  ngModule.component('queriesSearchResultsPage', {
    template,
    controller: QuerySearchCtrl,
  });

  return {
    '/queries/search': {
      template: '<queries-search-results-page></queries-search-results-page>',
      reloadOnSearch: true,
      title: 'Queries Search',
    },
  };
}
