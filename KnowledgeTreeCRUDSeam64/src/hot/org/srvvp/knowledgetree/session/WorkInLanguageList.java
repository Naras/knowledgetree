package org.srvvp.knowledgetree.session;

import org.srvvp.knowledgetree.entity.*;
import org.jboss.seam.annotations.Name;
import org.jboss.seam.framework.EntityQuery;
import java.util.Arrays;

@Name("workInLanguageList")
public class WorkInLanguageList extends EntityQuery<WorkInLanguage> {

	private static final String EJBQL = "select workInLanguage from WorkInLanguage workInLanguage";

	private static final String[] RESTRICTIONS = {
			"lower(workInLanguage.id.language) like lower(concat(#{workInLanguageList.workInLanguage.id.language},'%'))",
			"lower(workInLanguage.id.work) like lower(concat(#{workInLanguageList.workInLanguage.id.work},'%'))",
			"lower(workInLanguage.location) like lower(concat(#{workInLanguageList.workInLanguage.location},'%'))",};

	private WorkInLanguage workInLanguage;

	public WorkInLanguageList() {
		workInLanguage = new WorkInLanguage();
		workInLanguage.setId(new WorkInLanguageId());
		setEjbql(EJBQL);
		setRestrictionExpressionStrings(Arrays.asList(RESTRICTIONS));
		setMaxResults(25);
	}

	public WorkInLanguage getWorkInLanguage() {
		return workInLanguage;
	}
}
