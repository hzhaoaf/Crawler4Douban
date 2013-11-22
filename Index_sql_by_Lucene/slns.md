If you previously used Document.setBoost, you must now pre-multiply
> >>> the document boost into each Field.setBoost. If you have a
> >>> multi-valued field, you should do this only for the first Field
> >>> instance (ie, subsequent Field instance sharing the same field name
> >>> should only include their per-field boost and not the document level
> >>> boost) as the boost for multi-valued field instances are multiplied
> >>> together by Lucene."


You cannot set an index-time boost on an unindexed field, or one that omits norms

This exception ("You cannot set an index-time boost: norms are
omitted") was recently added to Lucene, to close a previous nasty trap
whereby you set boost but omitNorms on a given Field, and think the
boost is working, when in fact it was (previously) silently dropped.
Now you get an exception letting you know the boost won't work.

Here's the Lucene CHANGES entry (in Lucene 3.6.0):

* LUCENE-3796, SOLR-3241: Throw an exception if you try to set an index-time
  boost on a field that omits norms. Because the index-time boost
  is multiplied into the norm, previously your boost would be
  silently discarded.  (Tomás Fernández Löbbe, Hoss Man, Robert Muir)

I think ElasticSearch must turn off norms for a type: float field?  I
think instead you should set the boost on your text field(s)?
