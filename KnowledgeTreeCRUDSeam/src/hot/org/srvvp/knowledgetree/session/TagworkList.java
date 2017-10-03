package org.srvvp.knowledgetree.session;

import org.srvvp.knowledgetree.entity.*;
import org.jboss.seam.annotations.Name;
import org.jboss.seam.framework.EntityQuery;
import java.util.Arrays;

@Name("tagworkList")
public class TagworkList extends EntityQuery<Tagwork> {

	private static final String EJBQL = "select tagwork from Tagwork tagwork";

	private static final String[] RESTRICTIONS = {
			"lower(tagwork.id) like lower(concat(#{tagworkList.tagwork.id},'%'))",
			"lower(tagwork.name) like lower(concat(#{tagworkList.tagwork.name},'%'))",};

	private Tagwork tagwork = new Tagwork();

	public TagworkList() {
		setEjbql(EJBQL);
		setRestrictionExpressionStrings(Arrays.asList(RESTRICTIONS));
		setMaxResults(25);
	}

	public Tagwork getTagwork() {
		return tagwork;
	}
}
