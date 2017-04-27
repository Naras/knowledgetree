package org.srvvp.knowledgetree.session;

import org.srvvp.knowledgetree.entity.*;
import org.jboss.seam.annotations.Name;
import org.jboss.seam.framework.EntityQuery;
import java.util.Arrays;

@Name("workHasTagList")
public class WorkHasTagList extends EntityQuery<WorkHasTag> {

	private static final String EJBQL = "select workHasTag from WorkHasTag workHasTag";

	private static final String[] RESTRICTIONS = {
			"lower(workHasTag.id.tag) like lower(concat(#{workHasTagList.workHasTag.id.tag},'%'))",
			"lower(workHasTag.id.work) like lower(concat(#{workHasTagList.workHasTag.id.work},'%'))",};

	private WorkHasTag workHasTag;

	public WorkHasTagList() {
		workHasTag = new WorkHasTag();
		workHasTag.setId(new WorkHasTagId());
		setEjbql(EJBQL);
		setRestrictionExpressionStrings(Arrays.asList(RESTRICTIONS));
		setMaxResults(25);
	}

	public WorkHasTag getWorkHasTag() {
		return workHasTag;
	}
}
