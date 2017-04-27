package org.srvvp.knowledgetree.session;

import org.srvvp.knowledgetree.entity.*;
import org.jboss.seam.annotations.Name;
import org.jboss.seam.framework.EntityQuery;
import java.util.Arrays;

@Name("workRelatestoWorkList")
public class WorkRelatestoWorkList extends EntityQuery<WorkRelatestoWork> {

	private static final String EJBQL = "select workRelatestoWork from WorkRelatestoWork workRelatestoWork";

	private static final String[] RESTRICTIONS = {
			"lower(workRelatestoWork.id.work1) like lower(concat(#{workRelatestoWorkList.workRelatestoWork.id.work1},'%'))",
			"lower(workRelatestoWork.id.work2) like lower(concat(#{workRelatestoWorkList.workRelatestoWork.id.work2},'%'))",};

	private WorkRelatestoWork workRelatestoWork;

	public WorkRelatestoWorkList() {
		workRelatestoWork = new WorkRelatestoWork();
		workRelatestoWork.setId(new WorkRelatestoWorkId());
		setEjbql(EJBQL);
		setRestrictionExpressionStrings(Arrays.asList(RESTRICTIONS));
		setMaxResults(25);
	}

	public WorkRelatestoWork getWorkRelatestoWork() {
		return workRelatestoWork;
	}
}
