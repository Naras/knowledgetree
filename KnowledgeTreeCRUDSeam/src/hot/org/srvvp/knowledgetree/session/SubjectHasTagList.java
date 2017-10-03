package org.srvvp.knowledgetree.session;

import org.srvvp.knowledgetree.entity.*;
import org.jboss.seam.annotations.Name;
import org.jboss.seam.framework.EntityQuery;
import java.util.Arrays;

@Name("subjectHasTagList")
public class SubjectHasTagList extends EntityQuery<SubjectHasTag> {

	private static final String EJBQL = "select subjectHasTag from SubjectHasTag subjectHasTag";

	private static final String[] RESTRICTIONS = {
			"lower(subjectHasTag.id.subject) like lower(concat(#{subjectHasTagList.subjectHasTag.id.subject},'%'))",
			"lower(subjectHasTag.id.tag) like lower(concat(#{subjectHasTagList.subjectHasTag.id.tag},'%'))",};

	private SubjectHasTag subjectHasTag;

	public SubjectHasTagList() {
		subjectHasTag = new SubjectHasTag();
		subjectHasTag.setId(new SubjectHasTagId());
		setEjbql(EJBQL);
		setRestrictionExpressionStrings(Arrays.asList(RESTRICTIONS));
		setMaxResults(25);
	}

	public SubjectHasTag getSubjectHasTag() {
		return subjectHasTag;
	}
}
