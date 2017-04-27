package org.srvvp.knowledgetree.session;

import org.srvvp.knowledgetree.entity.*;
import org.jboss.seam.annotations.Name;
import org.jboss.seam.framework.EntityQuery;
import java.util.Arrays;

@Name("tagList")
public class TagList extends EntityQuery<Tag> {

	private static final String EJBQL = "select tag from Tag tag";

	private static final String[] RESTRICTIONS = {
			"lower(tag.id) like lower(concat(#{tagList.tag.id},'%'))",
			"lower(tag.name) like lower(concat(#{tagList.tag.name},'%'))",};

	private Tag tag = new Tag();

	public TagList() {
		setEjbql(EJBQL);
		setRestrictionExpressionStrings(Arrays.asList(RESTRICTIONS));
		setMaxResults(25);
	}

	public Tag getTag() {
		return tag;
	}
}
