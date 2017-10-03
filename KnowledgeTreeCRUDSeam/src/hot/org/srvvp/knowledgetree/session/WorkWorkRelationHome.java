package org.srvvp.knowledgetree.session;

import org.srvvp.knowledgetree.entity.*;
import java.util.ArrayList;
import java.util.List;
import org.jboss.seam.annotations.Name;
import org.jboss.seam.framework.EntityHome;

@Name("workWorkRelationHome")
public class WorkWorkRelationHome extends EntityHome<WorkWorkRelation> {

	public void setWorkWorkRelationId(String id) {
		setId(id);
	}

	public String getWorkWorkRelationId() {
		return (String) getId();
	}

	@Override
	protected WorkWorkRelation createInstance() {
		WorkWorkRelation workWorkRelation = new WorkWorkRelation();
		return workWorkRelation;
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

	public WorkWorkRelation getDefinedInstance() {
		return isIdDefined() ? getInstance() : null;
	}

	public List<WorkRelatestoWork> getWorkRelatestoWorks() {
		return getInstance() == null ? null : new ArrayList<WorkRelatestoWork>(
				getInstance().getWorkRelatestoWorks());
	}

}
