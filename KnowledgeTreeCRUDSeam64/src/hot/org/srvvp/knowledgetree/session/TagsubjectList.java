package org.srvvp.knowledgetree.session;

import org.srvvp.knowledgetree.entity.*;
import org.jboss.seam.annotations.Name;
import org.jboss.seam.framework.EntityQuery;
import java.util.Arrays;

@Name("tagsubjectList")
public class TagsubjectList extends EntityQuery<Tagsubject> {

	private static final String EJBQL = "select tagsubject from Tagsubject tagsubject";

	private static final String[] RESTRICTIONS = {
			"lower(tagsubject.id) like lower(concat(#{tagsubjectList.tagsubject.id},'%'))",
			"lower(tagsubject.name) like lower(concat(#{tagsubjectList.tagsubject.name},'%'))",};

	private Tagsubject tagsubject = new Tagsubject();

	public TagsubjectList() {
		setEjbql(EJBQL);
		setRestrictionExpressionStrings(Arrays.asList(RESTRICTIONS));
		setMaxResults(25);
	}

	public Tagsubject getTagsubject() {
		return tagsubject;
	}
}
