package org.srvvp.knowledgetree.session;

import org.srvvp.knowledgetree.entity.*;
import org.jboss.seam.annotations.Name;
import org.jboss.seam.framework.EntityQuery;
import java.util.Arrays;

@Name("workSubjectRelationList")
public class WorkSubjectRelationList extends EntityQuery<WorkSubjectRelation> {

	private static final String EJBQL = "select workSubjectRelation from WorkSubjectRelation workSubjectRelation";

	private static final String[] RESTRICTIONS = {
			"lower(workSubjectRelation.id) like lower(concat(#{workSubjectRelationList.workSubjectRelation.id},'%'))",
			"lower(workSubjectRelation.description) like lower(concat(#{workSubjectRelationList.workSubjectRelation.description},'%'))",
			"lower(workSubjectRelation.name) like lower(concat(#{workSubjectRelationList.workSubjectRelation.name},'%'))",};

	private WorkSubjectRelation workSubjectRelation = new WorkSubjectRelation();

	public WorkSubjectRelationList() {
		setEjbql(EJBQL);
		setRestrictionExpressionStrings(Arrays.asList(RESTRICTIONS));
		setMaxResults(25);
	}

	public WorkSubjectRelation getWorkSubjectRelation() {
		return workSubjectRelation;
	}
}
