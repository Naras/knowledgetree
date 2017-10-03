package org.srvvp.knowledgetree.session;

import org.srvvp.knowledgetree.entity.*;
import java.util.ArrayList;
import java.util.List;
import org.jboss.seam.annotations.Name;
import org.jboss.seam.framework.EntityHome;

@Name("workSubjectRelationHome")
public class WorkSubjectRelationHome extends EntityHome<WorkSubjectRelation> {

	public void setWorkSubjectRelationId(String id) {
		setId(id);
	}

	public String getWorkSubjectRelationId() {
		return (String) getId();
	}

	@Override
	protected WorkSubjectRelation createInstance() {
		WorkSubjectRelation workSubjectRelation = new WorkSubjectRelation();
		return workSubjectRelation;
	}

	public void load() {
		if (isIdDefined()) {
			wire();
		}
	}

	public void wire() {
		getInstance();
	}

	public boolean isWired() {
		return true;
	}

	public WorkSubjectRelation getDefinedInstance() {
		return isIdDefined() ? getInstance() : null;
	}

	public List<SubjectHasWork> getSubjectHasWorks() {
		return getInstance() == null ? null : new ArrayList<SubjectHasWork>(
				getInstance().getSubjectHasWorks());
	}

}
