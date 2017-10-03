package org.srvvp.knowledgetree.session;

import org.srvvp.knowledgetree.entity.*;
import org.jboss.seam.annotations.Name;
import org.jboss.seam.framework.EntityQuery;
import java.util.Arrays;

@Name("workWorkRelationList")
public class WorkWorkRelationList extends EntityQuery<WorkWorkRelation> {

	private static final String EJBQL = "select workWorkRelation from WorkWorkRelation workWorkRelation";

	private static final String[] RESTRICTIONS = {
			"lower(workWorkRelation.id) like lower(concat(#{workWorkRelationList.workWorkRelation.id},'%'))",
			"lower(workWorkRelation.description) like lower(concat(#{workWorkRelationList.workWorkRelation.description},'%'))",
			"lower(workWorkRelation.name) like lower(concat(#{workWorkRelationList.workWorkRelation.name},'%'))",};

	private WorkWorkRelation workWorkRelation = new WorkWorkRelation();

	public WorkWorkRelationList() {
		setEjbql(EJBQL);
		setRestrictionExpressionStrings(Arrays.asList(RESTRICTIONS));
		setMaxResults(25);
	}

	public WorkWorkRelation getWorkWorkRelation() {
		return workWorkRelation;
	}
}
