import json

from flask import request

from redash import models
from redash.handlers.base import BaseResource, get_object_or_404
from redash.permissions import (require_admin_or_owner,
                                require_object_modify_permission,
                                require_permission)


class VisualizationListResource(BaseResource):
    @require_permission('edit_query')
    def post(self):
        kwargs = request.get_json(force=True)

        query = get_object_or_404(models.Query.get_by_id_and_org, kwargs.pop('query_id'), self.current_org)
        require_object_modify_permission(query, self.current_user)

        kwargs['options'] = json.dumps(kwargs['options'])
        kwargs['query_rel'] = query

        vis = models.Visualization(**kwargs)
        models.db.session.add(vis)
        models.db.session.commit()
        d = vis.to_dict(with_query=False)
        return d


class VisualizationResource(BaseResource):
    @require_permission('edit_query')
    def post(self, visualization_id):
        vis = get_object_or_404(models.Visualization.get_by_id_and_org, visualization_id, self.current_org)
        require_object_modify_permission(vis.query_rel, self.current_user)

        kwargs = request.get_json(force=True)
        if 'options' in kwargs:
            kwargs['options'] = json.dumps(kwargs['options'])

        kwargs.pop('id', None)
        kwargs.pop('query_id', None)

        self.update_model(vis, kwargs)
        d = vis.to_dict(with_query=False)
        models.db.session.commit()
        return d

    @require_permission('edit_query')
    def delete(self, visualization_id):
        vis = get_object_or_404(models.Visualization.get_by_id_and_org, visualization_id, self.current_org)
        require_object_modify_permission(vis.query_rel, self.current_user)
        self.record_event({
            'action': 'delete',
            'object_id': visualization_id,
            'object_type': 'visualization',
        })
        models.db.session.delete(vis)
        models.db.session.commit()
