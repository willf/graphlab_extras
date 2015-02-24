#!/usr/bin/python -tt
# -*- coding: utf-8 -*-
""" 
    Code for cross validation.

    >>> import graphlab as gl
    >>> from graphlab_extras import cross_validate
    >>> data =  gl.SFrame.read_csv('http://s3.amazonaws.com/gl-testdata/xgboost/mushroom.csv')

   # Label 'p' is edible
   >>> data['label'] = data['label'] == 'p'
   >>> def cr_classify(train_data): return gl.boosted_trees_classifier.create(train_data, target='label')
   >>> def cr_regress(train_data): return gl.boosted_trees_regression.create(train_data, target='label')
   >>> cross_validate.cross_validate(cr_classify, data, folds=5)
   >>> cross_validate.cross_validate(cr_regress, data, folds=5)

"""
__author__ = "Will Fitzgerald"

import graphlab as gl


def _cross_validate_once(creator, data, split_percentage):
    train, test = data.random_split(split_percentage)
    return creator(train).evaluate(test)


def _cross_validate_many(creator, data, folds):
    return [_cross_validate_once(creator, data, (1.0 / folds) * (folds - 1)) for i in xrange(folds)]


def _combine(matrices):
    if not matrices:
        return []
    if len(matrices) == 1:
        return matrices[0]
    else:
        return _combine(
            [matrices[0].join(matrices[1], on=['target_label', 'predicted_label'], how='outer')] + matrices[2:])


def _combine_columns(frame, columns, column_name, combiner):
    keepers = [column for column in frame.column_names() if column not in columns]
    combined = [combiner([row[column] for column in columns]) for row in frame]
    d = dict()
    for k in keepers:
        d[k] = frame[k]
    d[column_name] = combined
    return gl.SFrame(d)


def _combine_confusion_matrices(matrices):
    def s(vs):
        return sum([v for v in vs if v]) / float(len(vs))  # might have Nones

    if not matrices:
        return matrices
    combined = _combine(matrices)
    count_columns = [name for name in combined.column_names() if name.startswith("count")]
    return _combine_columns(combined, count_columns, 'average_count', s)


def cross_validate(creator, data, folds=5):
    rs = _cross_validate_many(creator, data, folds)
    cfs = _combine_confusion_matrices([cf for cf in [r.get('confusion_matrix') for r in rs] if cf])
    d = dict()
    for key in [k for k in rs[0].keys() if type(rs[0][k]) == float]:
        d['average_%s' % key] = sum([r[k] for r in rs]) / len(rs)
    if cfs:
        d['confusion_matrix'] = cfs
    return d
