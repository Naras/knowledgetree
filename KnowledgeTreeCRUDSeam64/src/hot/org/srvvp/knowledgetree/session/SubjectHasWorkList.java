package org.srvvp.knowledgetree.session;

import org.srvvp.knowledgetree.entity.*;
import org.jboss.seam.annotations.Name;
import org.jboss.seam.framework.EntityQuery;
import java.util.Arrays;

@Name("subjectHasWorkList")
public class SubjectHasWorkList extends EntityQuery<SubjectHasWork> {

	private static final String EJBQL = "select subjectHasWork from SubjectHasWork subjectHasWork";

	private static final String[] RESTRICTIONS = {
			"lower(subjectHasWork.id.subject) like lower(concat(#{subjectHasWorkList.subjectHasWork.id.subject},'%'))",
			"lower(subjectHasWork.id.work) like lower(concat(#{subjectHasWorkList.subjectHasWork.id.work},'%'))",
			"lower(subjectHasWork.id.workSubjectRelation) like lower(concat(#{subjectHasWorkList.subjectHasWork.id.workSubjectRelation},'%'))",};

	private SubjectHasWork subjectHasWork;

	public SubjectHasWorkList() {
		subjectHasWork = new SubjectHasWork();
		subjectHasWork.setId(new SubjectHasWorkId());
		setEjbql(EJBQL);
		setRestrictionExpressionStrings(Arrays.asList(RESTRICTIONS));
		setMaxResults(25);
	}

	public SubjectHasWork getSubjectHasWork() {
		return subjectHasWork;
	}
}
