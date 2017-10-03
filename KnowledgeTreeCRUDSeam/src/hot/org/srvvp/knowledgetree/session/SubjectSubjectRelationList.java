package org.srvvp.knowledgetree.session;

import org.srvvp.knowledgetree.entity.*;
import org.jboss.seam.annotations.Name;
import org.jboss.seam.framework.EntityQuery;
import java.util.Arrays;

@Name("subjectSubjectRelationList")
public class SubjectSubjectRelationList
		extends
			EntityQuery<SubjectSubjectRelation> {

	private static final String EJBQL = "select subjectSubjectRelation from SubjectSubjectRelation subjectSubjectRelation";

	private static final String[] RESTRICTIONS = {
			"lower(subjectSubjectRelation.id) like lower(concat(#{subjectSubjectRelationList.subjectSubjectRelation.id},'%'))",
			"lower(subjectSubjectRelation.description) like lower(concat(#{subjectSubjectRelationList.subjectSubjectRelation.description},'%'))",
			"lower(subjectSubjectRelation.name) like lower(concat(#{subjectSubjectRelationList.subjectSubjectRelation.name},'%'))",};

	private SubjectSubjectRelation subjectSubjectRelation = new SubjectSubjectRelation();

	public SubjectSubjectRelationList() {
		setEjbql(EJBQL);
		setRestrictionExpressionStrings(Arrays.asList(RESTRICTIONS));
		setMaxResults(25);
	}

	public SubjectSubjectRelation getSubjectSubjectRelation() {
		return subjectSubjectRelation;
	}
}
